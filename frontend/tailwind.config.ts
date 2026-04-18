import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Fira Sans', 'ui-sans-serif', 'system-ui'],
        mono: ['Fira Code', 'ui-monospace', 'monospace'],
      },
      colors: {
        canvas: '#060D1B',
        surface: 'rgba(255,255,255,0.04)',
        'surface-hover': 'rgba(255,255,255,0.07)',
        rim: 'rgba(255,255,255,0.08)',
        'rim-bright': 'rgba(59,130,246,0.4)',
      },
      backgroundImage: {
        'canvas-grad':
          'radial-gradient(ellipse at 15% 60%, rgba(59,130,246,0.10) 0%, transparent 55%), radial-gradient(ellipse at 85% 15%, rgba(168,139,250,0.07) 0%, transparent 50%)',
      },
      boxShadow: {
        glass: '0 8px 32px rgba(0,0,0,0.45)',
        'glass-lg': '0 16px 48px rgba(0,0,0,0.55)',
        glow: '0 0 20px rgba(59,130,246,0.25)',
        'glow-amber': '0 0 20px rgba(245,158,11,0.25)',
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease forwards',
        'slide-in': 'slideIn 0.35s ease forwards',
        pulse: 'pulse 2s cubic-bezier(0.4,0,0.6,1) infinite',
      },
      keyframes: {
        fadeIn: { from: { opacity: '0', transform: 'translateY(8px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        slideIn: { from: { opacity: '0', transform: 'translateX(20px)' }, to: { opacity: '1', transform: 'translateX(0)' } },
      },
    },
  },
  plugins: [],
} satisfies Config
