/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./patients/**/*.{html,js}",
    "./templates/**/*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
}

