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
        "REJECTED": "#e5383b",
        "IN-PROGRESS": "#ffbe0b",
        "PENDING": "#fca311",
        "INCOMPLETE": "#e5383b",
        "COMPLETED": "#52b788",
      },
    },
  },
  plugins: [
    require("flowbite/plugin")
  ],
}

