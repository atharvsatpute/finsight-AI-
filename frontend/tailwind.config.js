/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Syne', 'sans-serif'],
        mono: ['DM Mono', 'monospace'],
      },
      colors: {
        bg: '#0b0f1a',
        surface: '#111827',
        surface2: '#1a2235',
        border: '#1e2d45',
        accent: '#00e5a0',
        accent2: '#7c6ef5',
        warn: '#f59e0b',
        danger: '#ef4444',
        muted: '#64748b',
      },
    },
  },
  plugins: [],
}
