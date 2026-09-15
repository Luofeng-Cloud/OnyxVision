/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        onyx: {
          bg: '#0A0B0E',
          surface: '#12141D',
          card: 'rgba(26, 29, 41, 0.65)',
          border: 'rgba(255, 255, 255, 0.08)',
          accent: '#a855f7',
          neon: '#6366f1',
          cyan: '#06b6d4',
          blue: '#007AFF',
          textMuted: '#8E8E93',
          badge: 'rgba(255, 255, 255, 0.12)'
        }
      },
      fontFamily: {
        apple: [
          "-apple-system",
          "BlinkMacSystemFont",
          "'SF Pro Display'",
          "'SF Pro Text'",
          "'PingFang SC'",
          "'Hiragino Sans GB'",
          "'Microsoft YaHei'",
          "sans-serif"
        ]
      },
      backdropBlur: {
        xs: '2px',
        onyx: '25px'
      },
      aspectRatio: {
        'poster': '2 / 3',
        'backdrop': '16 / 9',
        'hero': '21 / 9'
      }
    },
  },
  plugins: [],
}
