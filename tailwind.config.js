/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.{html,js}",
    "./src/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      fontFamily: {
        grotesk: ["SpaceGrotesk"],
      },
    },
    colors: {
      white: "#ffffff",
      black: "#000000",
      blue: {
        50: "#ecfcff",
        100: "#d4f7ff",
        200: "#b2f4ff",
        300: "#7defff",
        400: "#40e1ff",
        500: "#14c7ff",
        600: "#00a9ff",
        700: "#0091ff",
        800: "#0077d2",
        900: "#0861a0",
        950: "#0a3b61",
      },
    },
  },
  plugins: [require("flowbite/plugin")],
};
