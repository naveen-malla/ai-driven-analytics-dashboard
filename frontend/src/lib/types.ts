export interface ChartSpec {
  chart_id: string
  title: string
  chart_type: 'bar' | 'line' | 'area'
  x_key: string
  y_key: string
  data: Record<string, unknown>[]
  metric_definition: string
  x_label: string
  y_label: string
}

export interface ChartsResponse {
  charts: ChartSpec[]
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  chart?: ChartSpec
}

export interface ChatResponse {
  reply: string
  chart: ChartSpec | null
  intent: 'explain_chart' | 'new_analysis' | 'reject'
}

export const LOWER_IS_BETTER = new Set([
  'maternal_mortality',
  'under5_mortality',
  'hiv_prevalence',
])

export const CHART_COLORS = ['#3B82F6', '#F59E0B', '#10B981', '#A78BFA', '#F43F5E']
export const LOWER_COLORS = ['#10B981', '#22C55E', '#F59E0B', '#F97316', '#EF4444']
