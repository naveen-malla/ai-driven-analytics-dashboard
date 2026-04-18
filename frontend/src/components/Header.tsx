import { MessageSquare, LayoutDashboard, Activity } from 'lucide-react'
import clsx from 'clsx'

interface Props {
  backendOk: boolean
  chatOpen: boolean
  sidebarOpen: boolean
  onToggleChat: () => void
  onToggleSidebar: () => void
}

export default function Header({ backendOk, chatOpen, sidebarOpen, onToggleChat, onToggleSidebar }: Props) {
  const now = new Date()
  const dateStr = now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })

  return (
    <header className="glass shrink-0 border-b border-white/[0.07] px-5 py-3">
      <div className="flex items-center gap-4">
        {/* Logo */}
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600/20 ring-1 ring-blue-500/30">
            <Activity className="h-4 w-4 text-blue-400" />
          </div>
          <div className="leading-tight">
            <p className="text-sm font-semibold text-slate-100 tracking-tight">HealthAnalytics</p>
            <p className="text-[10px] font-medium text-slate-500 uppercase tracking-widest">AI Copilot</p>
          </div>
        </div>

        <div className="mx-4 h-6 w-px bg-white/[0.08]" />

        {/* Status indicators */}
        <div className="flex items-center gap-4">
          <StatusDot label="Backend" ok={backendOk} />
          <StatusDot label="Data" ok={true} />
          <StatusDot label="AI" ok={true} />
        </div>

        <div className="flex-1" />

        {/* Date */}
        <span className="hidden text-xs text-slate-500 sm:block font-mono">{dateStr}</span>

        <div className="mx-3 h-6 w-px bg-white/[0.08]" />

        {/* Toggle buttons */}
        <button
          className={clsx('btn-ghost', sidebarOpen && 'text-blue-400 bg-blue-500/10')}
          onClick={onToggleSidebar}
          aria-label="Toggle sidebar"
        >
          <LayoutDashboard className="h-4 w-4" />
        </button>
        <button
          className={clsx('btn-ghost', chatOpen && 'text-blue-400 bg-blue-500/10')}
          onClick={onToggleChat}
          aria-label="Toggle chat"
        >
          <MessageSquare className="h-4 w-4" />
        </button>
      </div>
    </header>
  )
}

function StatusDot({ label, ok }: { label: string; ok: boolean }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className={clsx('relative flex h-2 w-2')}>
        <span className={clsx('absolute inline-flex h-full w-full animate-ping rounded-full opacity-50',
          ok ? 'bg-emerald-400' : 'bg-red-400')} />
        <span className={clsx('relative inline-flex h-2 w-2 rounded-full',
          ok ? 'bg-emerald-400' : 'bg-red-400')} />
      </span>
      <span className="hidden text-[11px] text-slate-500 sm:block">{label}</span>
    </div>
  )
}
