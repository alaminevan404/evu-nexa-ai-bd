/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: '#04070D',
          900: '#090D16',
          850: '#0E1422',
          800: '#141C2E',
          700: '#1F2B44',
          600: '#2D3D5E'
        },
        nexa: {
          cyan: '#00F2FE',
          blue: '#4FACFE',
          violet: '#7F00FF',
          purple: '#E100FF',
          emerald: '#00E676',
          crimson: '#FF1744',
          amber: '#FFAB00'
        },
        glass: {
          surface: 'rgba(14, 20, 34, 0.70)',
          border: 'rgba(255, 255, 255, 0.08)',
          glow: 'rgba(0, 242, 254, 0.15)'
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      },
      boxShadow: {
        'cyan-glow': '0 0 25px -5px rgba(0, 242, 254, 0.4)',
        'violet-glow': '0 0 25px -5px rgba(127, 0, 255, 0.4)',
        'bullish-glow': '0 0 30px -5px rgba(0, 230, 118, 0.4)',
        'bearish-glow': '0 0 30px -5px rgba(255, 23, 68, 0.4)',
        'glass-card': '0 8px 32px 0 rgba(0, 0, 0, 0.37)'
      }
    },
  },
  plugins: [],
}
