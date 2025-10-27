// /** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx}',
    './public/index.html'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1e40af',
        secondary: '#10b981',
        accent: '#f59e0b'
      },
      fontFamily: {
        inter: ['Inter', 'system-ui', 'sans-serif']
      }
    }
  },
  plugins: []
};
