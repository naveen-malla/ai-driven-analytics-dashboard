import { useEffect, useState } from 'react'
import { fetchCharts } from './lib/api'
import type { ChartSpec, ChatMessage } from './lib/types'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import ChartsGrid from './components/ChartsGrid'
import ChatPanel from './components/ChatPanel'
import LoadingSkeleton from './components/LoadingSkeleton'

export default function App() {
  const [charts, setCharts] = useState<ChartSpec[]>([])
  const [loading, setLoading] = useState(true)
  const [backendError, setBackendError] = useState(false)
  const [selectedChartId, setSelectedChartId] = useState<string | undefined>()
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])
  const [chatOpen, setChatOpen] = useState(true)
  const [sidebarOpen, setSidebarOpen] = useState(true)

  useEffect(() => {
    fetchCharts()
      .then(setCharts)
      .catch(() => setBackendError(true))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div
      className="flex h-screen flex-col overflow-hidden bg-canvas bg-canvas-grad"
      style={{ fontFamily: "'Fira Sans', sans-serif" }}
    >
      <Header
        backendOk={!backendError}
        chatOpen={chatOpen}
        sidebarOpen={sidebarOpen}
        onToggleChat={() => setChatOpen((v) => !v)}
        onToggleSidebar={() => setSidebarOpen((v) => !v)}
      />

      <div className="flex flex-1 overflow-hidden">
        {sidebarOpen && (
          <Sidebar
            charts={charts}
            selectedChartId={selectedChartId}
            onSelectChart={setSelectedChartId}
          />
        )}

        <main className="flex-1 overflow-y-auto px-6 py-5">
          {loading ? (
            <LoadingSkeleton />
          ) : backendError ? (
            <BackendErrorBanner />
          ) : (
            <ChartsGrid
              charts={charts}
              selectedChartId={selectedChartId}
              onSelectChart={(id) => {
                setSelectedChartId(id)
                setChatOpen(true)
              }}
            />
          )}
        </main>

        {chatOpen && (
          <ChatPanel
            selectedChart={charts.find((c) => c.chart_id === selectedChartId)}
            history={chatHistory}
            onHistory={setChatHistory}
          />
        )}
      </div>
    </div>
  )
}

function BackendErrorBanner() {
  return (
    <div className="flex h-full items-center justify-center">
      <div className="glass rounded-2xl p-10 text-center shadow-glass max-w-md">
        <div className="mb-4 inline-flex h-14 w-14 items-center justify-center rounded-full bg-red-50">
          <svg className="h-7 w-7 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
              d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
          </svg>
        </div>
        <p className="text-lg font-semibold text-slate-800">Backend Unreachable</p>
        <p className="mt-2 text-sm text-slate-500">
          Start the FastAPI server with <code className="font-mono text-blue-600">make backend</code> and refresh.
        </p>
      </div>
    </div>
  )
}
