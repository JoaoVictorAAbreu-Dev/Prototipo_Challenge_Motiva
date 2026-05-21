/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sentinel: {
          50: "#f8f9ff",
          100: "#f1f2ff",
          200: "#e3e6ff",
          300: "#d5d9ff",
          400: "#b8c1ff",
          500: "#9aabff",
          600: "#7d94ff",
          700: "#5f7dff",
          800: "#4166ff",
          900: "#2451cc",
        },
      },
    },
  },
  plugins: [],
}
