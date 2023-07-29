import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  build: {
    outDir: resolve(__dirname, "./dist"),
    assetsDir: "assets",
    emptyOutDir: true,
    assetsInlineLimit: 0,
    rollupOptions: {
      output: {
        assetFileNames: "public/[name][extname]",
      },
      input: {
        main: resolve(__dirname, "index.html"),
        login: resolve(__dirname, "login.html"),
        signup: resolve(__dirname, "signup.html"),
        auth: resolve(__dirname, "2fa.html"),
        dash: resolve(__dirname, "dashboard.html"),
        flowbite: resolve(
          __dirname,
          "./node_modules/flowbite/dist/flowbite.min.js"
        ),
        // Add more entries for any additional HTML files you want to include
      },
    },
  },
});
