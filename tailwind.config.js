/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./app/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        themis: {
          950: '#020617', // Very dark slate
          900: '#0f172a', // Deep slate
          800: '#1e293b', // Dark slate
          accent: '#06b6d4', // Cyan
          glow: '#6366f1', // Indigo
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in-up': 'fadeInUp 0.5s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
