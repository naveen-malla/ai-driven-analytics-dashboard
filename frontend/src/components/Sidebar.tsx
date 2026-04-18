import clsx from 'clsx'
import type { ChartSpec } from '../lib/types'
import { LOWER_IS_BETTER } from '../lib/types'

const ICONS: Record<string, string> = {
  contraceptive_prevalence: '♀',
  maternal_mortality: '♥',
  antenatal_care: '✚',
  skilled_birth: '★',
  under5_mortality: '◆',
  hiv_prevalence: '⬡',
}

interface Props {
  charts: ChartSpec[]
  selectedChartId: string | undefined
  onSelectChart: (id: string) => void
}

export default function Sidebar({ charts, selectedChartId, onSelectChart }: Props) {
  return (
    <aside className="glass flex w-56 shrink-0 flex-col border-r border-white/[0.07] overflow-y-auto">
      <div className="px-4 pt-5 pb-3">
        <p className="text-[10px] font-semibold uppercase tracking-widest text-slate-500">
          Indicators
        </p>
      </div>

      <nav className="flex-1 space-y-0.5 px-2 pb-4">
        {charts.map((chart) => {
          const lower = LOWER_IS_BETTER.has(chart.chart_id)
          const active = chart.chart_id === selectedChartId
          return (
            <button
              key={chart.chart_id}
              onClick={() => onSelectChart(chart.chart_id)}
              className={clsx(
                'w-full cursor-pointer rounded-lg px-3 py-2.5 text-left transition-all duration-150',
                'flex items-start gap-2.5 group',
                active
                  ? 'bg-blue-600/15 ring-1 ring-blue-500/30 text-slate-100'
                  : 'text-slate-400 hover:bg-white/[0.05] hover:text-slate-200',
              )}
            >
              <span className="mt-0.5 shrink-0 text-sm opacity-70">{ICONS[chart.chart_id] ?? '◉'}</span>
              <span className="flex-1 min-w-0">
                <span className="block text-xs font-medium leading-snug truncate">{chart.title}</span>
                <span className={clsx(
                  'mt-1 inline-flex items-center rounded-full px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wide',
                  lower
                    ? 'bg-emerald-500/10 text-emerald-400'
                    : 'bg-blue-500/10 text-blue-400',
                )}>
                  {lower ? '↓ lower' : '↑ higher'}
                </span>
              </span>
            </button>
          )
        })}
      </nav>

      <div className="border-t border-white/[0.07] px-4 py-3">
        <p className="text-[9px] font-medium uppercase tracking-widest text-slate-600">
          WHO GHO · 5 countries
        </p>
      </div>
    </aside>
  )
}
