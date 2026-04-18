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
        canvas: '#F1F5F9',
        surface: '#FFFFFF',
        'surface-hover': '#F8FAFC',
        rim: '#E2E8F0',
        'rim-bright': 'rgba(37,99,235,0.35)',
      },
      backgroundImage: {
        'canvas-grad':
          'radial-gradient(ellipse at 15% 60%, rgba(37,99,235,0.05) 0%, transparent 55%), radial-gradient(ellipse at 85% 15%, rgba(124,58,237,0.03) 0%, transparent 50%)',
      },
      boxShadow: {
        glass: '0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04)',
        'glass-lg': '0 4px 12px rgba(0,0,0,0.08), 0 16px 32px rgba(0,0,0,0.06)',
        glow: '0 0 0 3px rgba(37,99,235,0.12)',
        'glow-amber': '0 0 0 3px rgba(217,119,6,0.12)',
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
