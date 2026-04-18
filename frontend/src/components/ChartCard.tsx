import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { MessageSquare, ChevronDown, ChevronUp } from 'lucide-react'
import clsx from 'clsx'
import type { ChartSpec } from '../lib/types'
import { LOWER_IS_BETTER, CHART_COLORS, LOWER_COLORS } from '../lib/types'

interface Props {
  chart: ChartSpec
  selected: boolean
  onAskAI: () => void
}

export default function ChartCard({ chart, selected, onAskAI }: Props) {
  const [expanded, setExpanded] = useState(false)
  const isLower = LOWER_IS_BETTER.has(chart.chart_id)
  const colors = isLower ? LOWER_COLORS : CHART_COLORS

  return (
    <div
      className={clsx(
        'glass glass-hover rounded-2xl p-5 shadow-glass flex flex-col gap-4 transition-all duration-200',
        selected && 'ring-1 ring-blue-500/50 shadow-glow',
      )}
    >
      {/* Card header */}
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-sm font-semibold text-slate-100 leading-snug">{chart.title}</h3>
          <span className={clsx(
            'mt-1 badge',
            isLower
              ? 'bg-emerald-500/10 text-emerald-400 ring-1 ring-emerald-500/20'
              : 'bg-blue-500/10 text-blue-400 ring-1 ring-blue-500/20',
          )}>
            {isLower ? '↓ Lower is better' : '↑ Higher is better'}
          </span>
        </div>
        <button
          className="btn-primary flex items-center gap-1.5 shrink-0"
          onClick={onAskAI}
          aria-label={`Ask AI about ${chart.title}`}
        >
          <MessageSquare className="h-3.5 w-3.5" />
          <span>Ask AI</span>
        </button>
      </div>

      {/* Chart */}
      <div style={{ height: 220 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chart.data} margin={{ top: 4, right: 8, left: -8, bottom: 4 }}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(255,255,255,0.05)"
              vertical={false}
            />
            <XAxis
              dataKey={chart.x_key}
              tick={{ fill: '#94A3B8', fontSize: 11, fontFamily: 'Fira Sans' }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: '#94A3B8', fontSize: 11, fontFamily: 'Fira Sans' }}
              axisLine={false}
              tickLine={false}
              width={42}
              label={{
                value: chart.y_label,
                angle: -90,
                position: 'insideLeft',
                offset: 12,
                style: { fill: '#64748B', fontSize: 10, fontFamily: 'Fira Sans' },
              }}
            />
            <Tooltip content={<CustomTooltip yLabel={chart.y_label} />} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
            <Bar dataKey={chart.y_key} radius={[4, 4, 0, 0]} maxBarSize={48} isAnimationActive>
              {chart.data.map((_, index) => (
                <Cell key={index} fill={colors[index % colors.length]} fillOpacity={0.85} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Metric definition toggle */}
      <button
        className="flex w-full cursor-pointer items-center justify-between rounded-lg px-3 py-2 text-left
                   text-xs text-slate-500 hover:bg-white/[0.04] hover:text-slate-400 transition-colors duration-150"
        onClick={() => setExpanded((v) => !v)}
      >
        <span className="font-medium">Metric definition</span>
        {expanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
      </button>
      {expanded && (
        <p className="px-3 pb-1 text-xs leading-relaxed text-slate-400">{chart.metric_definition}</p>
      )}
    </div>
  )
}

function CustomTooltip({ active, payload, label, yLabel }: {
  active?: boolean
  payload?: { value: number }[]
  label?: string
  yLabel: string
}) {
  if (!active || !payload?.length) return null
  return (
    <div className="glass rounded-xl px-3 py-2 shadow-glass-lg text-xs">
      <p className="font-semibold text-slate-200">{label}</p>
      <p className="mt-0.5 font-mono text-blue-300">
        {payload[0].value.toFixed(1)} <span className="text-slate-500">{yLabel}</span>
      </p>
    </div>
  )
}
