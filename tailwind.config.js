/** @type {import("tailwindcss").Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        "CREATED": "#06D6A0",
        "CANCELLED": "#ad2831",
        "ACCEPTED": "#118AB2",
        "REJECTED": "#ad2831",
        "IN-PROGRESS": "#FFD166",
        "PENDING": "#fca311",
        "INCOMPLETE": "#d62828",
        "COMPLETED": "#008000",
      },
    },
  },
  plugins: [
    require("flowbite/plugin")
  ],
}

