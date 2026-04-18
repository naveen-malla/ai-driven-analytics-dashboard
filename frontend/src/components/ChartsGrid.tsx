import type { ChartSpec } from '../lib/types'
import ChartCard from './ChartCard'

interface Props {
  charts: ChartSpec[]
  selectedChartId: string | undefined
  onSelectChart: (id: string) => void
}

export default function ChartsGrid({ charts, selectedChartId, onSelectChart }: Props) {
  if (charts.length === 0) {
    return (
      <div className="flex h-64 items-center justify-center text-slate-500 text-sm">
        No chart data available.
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
      {charts.map((chart, i) => (
        <div
          key={chart.chart_id}
          className="animate-fade-in"
          style={{ animationDelay: `${i * 60}ms`, animationFillMode: 'both' }}
        >
          <ChartCard
            chart={chart}
            selected={chart.chart_id === selectedChartId}
            onAskAI={() => onSelectChart(chart.chart_id)}
          />
        </div>
      ))}
    </div>
  )
}
