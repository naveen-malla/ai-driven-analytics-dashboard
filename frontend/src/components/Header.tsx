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
    <header className="bg-white shrink-0 border-b border-slate-200 shadow-sm px-5 py-3">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2.5">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 ring-1 ring-blue-200">
            <Activity className="h-4 w-4 text-blue-600" />
          </div>
          <div className="leading-tight">
            <p className="text-sm font-semibold text-slate-800 tracking-tight">HealthAnalytics</p>
            <p className="text-[10px] font-medium text-slate-400 uppercase tracking-widest">AI Copilot</p>
          </div>
        </div>

        <div className="mx-4 h-6 w-px bg-slate-200" />

        <div className="flex items-center gap-4">
          <StatusDot label="Backend" ok={backendOk} />
          <StatusDot label="Data" ok={true} />
          <StatusDot label="AI" ok={true} />
        </div>

        <div className="flex-1" />

        <span className="hidden text-xs text-slate-400 sm:block font-mono">{dateStr}</span>

        <div className="mx-3 h-6 w-px bg-slate-200" />

        <button
          className={clsx('btn-ghost', sidebarOpen && 'text-blue-600 bg-blue-50')}
          onClick={onToggleSidebar}
          aria-label="Toggle sidebar"
        >
          <LayoutDashboard className="h-4 w-4" />
        </button>
        <button
          className={clsx('btn-ghost', chatOpen && 'text-blue-600 bg-blue-50')}
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
      <span className="relative flex h-2 w-2">
        <span className={clsx('absolute inline-flex h-full w-full animate-ping rounded-full opacity-50',
          ok ? 'bg-emerald-400' : 'bg-red-400')} />
        <span className={clsx('relative inline-flex h-2 w-2 rounded-full',
          ok ? 'bg-emerald-500' : 'bg-red-500')} />
      </span>
      <span className="hidden text-[11px] text-slate-500 sm:block">{label}</span>
    </div>
  )
}
