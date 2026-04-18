import { useRef, useState, useEffect } from 'react'
import { Send, Bot, User, Sparkles } from 'lucide-react'
import clsx from 'clsx'
import { sendChat } from '../lib/api'
import type { ChartSpec, ChatMessage } from '../lib/types'
import MiniChart from './MiniChart'

interface Props {
  selectedChart: ChartSpec | undefined
  history: ChatMessage[]
  onHistory: (fn: (prev: ChatMessage[]) => ChatMessage[]) => void
}

export default function ChatPanel({ selectedChart, history, onHistory }: Props) {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [history, loading])

  async function handleSend() {
    const msg = input.trim()
    if (!msg || loading) return
    setInput('')
    onHistory((prev) => [...prev, { role: 'user', content: msg }])
    setLoading(true)
    try {
      const res = await sendChat(msg, selectedChart?.chart_id)
      onHistory((prev) => [
        ...prev,
        { role: 'assistant', content: res.reply, chart: res.chart ?? undefined },
      ])
    } catch {
      onHistory((prev) => [
        ...prev,
        { role: 'assistant', content: 'Backend unavailable. Please start the API server.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  const placeholder = selectedChart
    ? `Ask about "${selectedChart.title}"…`
    : 'Ask a health analytics question…'

  return (
    <aside className="bg-slate-50 flex w-96 shrink-0 flex-col border-l border-slate-200">
      <div className="flex items-center gap-2.5 border-b border-slate-200 bg-white px-4 py-3.5">
        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-violet-50 ring-1 ring-violet-200">
          <Sparkles className="h-3.5 w-3.5 text-violet-600" />
        </div>
        <div>
          <p className="text-xs font-semibold text-slate-800">Health Copilot</p>
          {selectedChart && (
            <p className="text-[10px] text-slate-500 truncate max-w-[200px]">
              Context: {selectedChart.title}
            </p>
          )}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {history.length === 0 && <EmptyState />}
        {history.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      <div className="border-t border-slate-200 bg-white px-4 py-3">
        <div className="flex items-end gap-2">
          <textarea
            className="flex-1 resize-none rounded-xl bg-slate-50 border border-slate-200 px-3 py-2.5
                       text-sm text-slate-800 placeholder:text-slate-400 outline-none
                       focus:border-blue-400 focus:bg-white transition-colors duration-150
                       font-sans leading-relaxed max-h-32"
            rows={1}
            placeholder={placeholder}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSend()
              }
            }}
          />
          <button
            className={clsx(
              'shrink-0 flex h-10 w-10 cursor-pointer items-center justify-center rounded-xl transition-all duration-150',
              input.trim() && !loading
                ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-sm'
                : 'bg-slate-100 text-slate-400 cursor-not-allowed',
            )}
            onClick={handleSend}
            disabled={!input.trim() || loading}
            aria-label="Send message"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        <p className="mt-2 text-[10px] text-slate-400">
          Enter to send · Shift+Enter for new line
        </p>
      </div>
    </aside>
  )
}

function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user'
  return (
    <div className={clsx('flex gap-2.5', isUser && 'flex-row-reverse')}>
      <div className={clsx(
        'flex h-7 w-7 shrink-0 items-center justify-center rounded-full ring-1',
        isUser
          ? 'bg-blue-600 ring-blue-700 text-white'
          : 'bg-violet-50 ring-violet-200 text-violet-600',
      )}>
        {isUser ? <User className="h-3.5 w-3.5" /> : <Bot className="h-3.5 w-3.5" />}
      </div>
      <div className={clsx('max-w-[82%] space-y-2', isUser && 'items-end flex flex-col')}>
        <div className={clsx(
          'rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed',
          isUser
            ? 'bg-blue-600 text-white rounded-tr-sm'
            : 'bg-white text-slate-700 rounded-tl-sm shadow-sm ring-1 ring-slate-200',
        )}>
          {message.content}
        </div>
        {message.chart && (
          <div className="w-full bg-white rounded-xl p-3 shadow-sm ring-1 ring-slate-200">
            <p className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
              {message.chart.title}
            </p>
            <MiniChart chart={message.chart} />
          </div>
        )}
      </div>
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="flex gap-2.5">
      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-violet-50 ring-1 ring-violet-200">
        <Bot className="h-3.5 w-3.5 text-violet-600" />
      </div>
      <div className="flex items-center gap-1 rounded-2xl rounded-tl-sm bg-white px-4 py-3 shadow-sm ring-1 ring-slate-200">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="h-1.5 w-1.5 rounded-full bg-slate-300 animate-pulse"
            style={{ animationDelay: `${i * 200}ms` }}
          />
        ))}
      </div>
    </div>
  )
}

function EmptyState() {
  const suggestions = [
    'Compare maternal mortality across countries',
    'Which country has highest HIV prevalence?',
    'Show contraceptive use trends',
  ]
  return (
    <div className="space-y-4 py-2">
      <div className="text-center">
        <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-50 ring-1 ring-violet-200">
          <Sparkles className="h-6 w-6 text-violet-600" />
        </div>
        <p className="text-sm font-medium text-slate-700">Ask anything about health data</p>
        <p className="mt-1 text-xs text-slate-400">WHO data across 5 East African countries</p>
      </div>
      <div className="space-y-2">
        {suggestions.map((s) => (
          <button key={s} className="w-full cursor-default rounded-xl bg-white px-3 py-2 text-left text-xs text-slate-500 shadow-sm ring-1 ring-slate-200">
            {s}
          </button>
        ))}
      </div>
    </div>
  )
}
