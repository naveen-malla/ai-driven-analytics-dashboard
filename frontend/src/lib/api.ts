import type { ChartSpec, ChatResponse } from './types'

export async function fetchCharts(): Promise<ChartSpec[]> {
  const res = await fetch('/charts')
  if (!res.ok) throw new Error(`Backend error ${res.status}`)
  const body = await res.json()
  return body.charts as ChartSpec[]
}

export async function sendChat(message: string, chartId?: string): Promise<ChatResponse> {
  const res = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, chart_id: chartId ?? null }),
  })
  if (!res.ok) throw new Error(`Chat error ${res.status}`)
  return res.json() as Promise<ChatResponse>
}
