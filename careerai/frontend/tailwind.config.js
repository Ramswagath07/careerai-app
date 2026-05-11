/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#6c63ff', dark: '#5a52e0' },
        accent:  { pink: '#ff6b9d', teal: '#00d4aa', amber: '#ffb347' },
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        body: ['DM Sans', 'sans-serif'],
      },
    }
  },
  plugins: [],
}
