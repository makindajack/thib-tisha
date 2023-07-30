from __future__ import print_function
from flask import (
    Flask,
    render_template,
    request,
    session,
    Response,
)
import mysql.connector
import bcrypt
import random


app = Flask(__name__)
gcode = 0
app.secret_key = "mysup3rs3cr3tk3y"


def send2fa_prompt():
    # works with both python 2 and 3
    import africastalking

    username = "username"
    api_key = "YOUR-API-KEY"

    africastalking.initialize(username, api_key)

    # Get the SMS service
    sms = africastalking.SMS

    # Set the numbers you want to send to in international format
    recipients = ["+255755100100"]

    # Set your message
    message = "Authorize login"

    # Set your shortCode or senderId
    sender = "90762"
    try:
        # Thats it, hit send and we'll take care of the rest.
        response = sms.send(message, recipients, sender)
        print(response)

    except Exception as e:
        print("Encountered an error while sending: %s" % str(e))


# Configure the database connection
db_connection = mysql.connector.connect(
    host="localhost", user="root", password="", database="2fa"
)

db_cursor = db_connection.cursor()


# Homepage route
@app.route("/")
def index2():
    return render_template("index.html")


# Route for login form
@app.route("/authenticate")
def authme2():
    return render_template("login.html")


@app.route("/logout")
def logoutpage():
    phone = session.get("phone")
    update_query = "UPDATE users SET login = %s WHERE phone = %s"
    db_cursor.execute(update_query, (0, phone))
    db_connection.commit()
    return render_template("login.html")


# Route for the homepage (login form)
@app.route("/login", methods=["POST", "GET"])
def letmein():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if authenticate(username, password):
            session["username"] = username
            send2fa_prompt()
            code = random.randint(100000, 999999)
            update_query = "UPDATE users SET code = %s WHERE email = %s"
            db_cursor.execute(update_query, (code, username))
            db_connection.commit()

            return render_template("2fa.html", code=code, username=username)
        else:
            return render_template("login.html")
    return render_template("login.html")


# Route for the dashboard (successful login)
@app.route("/auth", methods=["GET"])
def authme():
    username = request.args.get("username")
    print(username)
    db_cursor.execute("SELECT login FROM users WHERE email = %s", (username,))
    if db_cursor.fetchone()[0] == 1:
        fname = session.get("fname") + " " + session.get("lname")
        phone = session.get("phone")
        return render_template("dashboard.html", name=fname, phone=phone)
    else:
        return render_template("login.html")


@app.route("/incoming-messages", methods=["POST"])
def incoming_messages():
    print(request.form["from"])
    print(request.form["text"])
    db_cursor.execute(
        "SELECT code FROM users WHERE phone = %s", (request.form["from"],)
    )
    if db_cursor.fetchone()[0] == request.form["text"]:
        session["phone"] = request.form["from"]

        update_query = "UPDATE users SET login = %s WHERE phone = %s"
        db_cursor.execute(update_query, (1, request.form["from"]))
        db_connection.commit()

    return Response(status=200)


def authenticate(username, password):
    # Fetch user data from the database
    db_cursor.execute(
        "SELECT password, phone, first_name, last_name FROM users WHERE email = %s",
        (username,),
    )
    user_data = db_cursor.fetchone()
    session["fname"] = user_data[2]
    session["lname"] = user_data[3]
    session["phone"] = user_data[1]
    print(user_data[0])
    # if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data[0]):
    if user_data and bcrypt.checkpw(
        password.encode("utf-8"), user_data[0].encode("utf-8")
    ):
        return True
    return False


if __name__ == "__main__":
    app.run(debug=True)
