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
    <aside className="bg-white flex w-56 shrink-0 flex-col border-r border-slate-200 shadow-sm overflow-y-auto">
      <div className="px-4 pt-5 pb-3">
        <p className="text-[10px] font-semibold uppercase tracking-widest text-slate-400">
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
                'flex items-start gap-2.5',
                active
                  ? 'bg-blue-50 ring-1 ring-blue-200 text-slate-800'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-800',
              )}
            >
              <span className="mt-0.5 shrink-0 text-sm text-slate-400">{ICONS[chart.chart_id] ?? '◉'}</span>
              <span className="flex-1 min-w-0">
                <span className="block text-xs font-medium leading-snug truncate">{chart.title}</span>
                <span className={clsx(
                  'mt-1 inline-flex items-center rounded-full px-1.5 py-0.5 text-[9px] font-semibold uppercase tracking-wide',
                  lower
                    ? 'bg-emerald-50 text-emerald-700 ring-1 ring-emerald-200'
                    : 'bg-blue-50 text-blue-700 ring-1 ring-blue-200',
                )}>
                  {lower ? '↓ lower' : '↑ higher'}
                </span>
              </span>
            </button>
          )
        })}
      </nav>

      <div className="border-t border-slate-200 px-4 py-3">
        <p className="text-[9px] font-medium uppercase tracking-widest text-slate-400">
          WHO GHO · 5 countries
        </p>
      </div>
    </aside>
  )
}
