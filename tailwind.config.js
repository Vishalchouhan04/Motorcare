/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}", "./static/**/*.js",   // ✅ All your Flask HTML templates
    "./app/**/*.py"            // ✅ Optional: scan your Python files for class names
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
