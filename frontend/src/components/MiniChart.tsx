import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Cell, Tooltip } from 'recharts'
import type { ChartSpec } from '../lib/types'
import { LOWER_IS_BETTER, CHART_COLORS, LOWER_COLORS } from '../lib/types'

export default function MiniChart({ chart }: { chart: ChartSpec }) {
  const colors = LOWER_IS_BETTER.has(chart.chart_id) ? LOWER_COLORS : CHART_COLORS
  return (
    <div style={{ height: 120 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chart.data} margin={{ top: 2, right: 4, left: -20, bottom: 0 }}>
          <XAxis dataKey={chart.x_key} tick={{ fill: '#64748B', fontSize: 9 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: '#64748B', fontSize: 9 }} axisLine={false} tickLine={false} width={30} />
          <Tooltip
            content={({ active, payload, label }) =>
              active && payload?.length ? (
                <div className="glass rounded-lg px-2 py-1 text-[10px]">
                  <span className="font-semibold text-slate-200">{label}</span>
                  {' · '}
                  <span className="font-mono text-blue-300">{(payload[0].value as number).toFixed(1)}</span>
                </div>
              ) : null
            }
            cursor={{ fill: 'rgba(255,255,255,0.03)' }}
          />
          <Bar dataKey={chart.y_key} radius={[3, 3, 0, 0]} maxBarSize={32}>
            {chart.data.map((_, i) => (
              <Cell key={i} fill={colors[i % colors.length]} fillOpacity={0.8} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
