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
    <aside className="glass flex w-96 shrink-0 flex-col border-l border-white/[0.07]">
      {/* Panel header */}
      <div className="flex items-center gap-2.5 border-b border-white/[0.07] px-4 py-3.5">
        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-violet-500/15 ring-1 ring-violet-500/25">
          <Sparkles className="h-3.5 w-3.5 text-violet-400" />
        </div>
        <div>
          <p className="text-xs font-semibold text-slate-200">Health Copilot</p>
          {selectedChart && (
            <p className="text-[10px] text-slate-500 truncate max-w-[200px]">
              Context: {selectedChart.title}
            </p>
          )}
        </div>
      </div>

      {/* Message history */}
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {history.length === 0 && (
          <EmptyState />
        )}
        {history.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="border-t border-white/[0.07] px-4 py-3">
        <div className="flex items-end gap-2">
          <textarea
            className="flex-1 resize-none rounded-xl bg-white/[0.05] border border-white/[0.08] px-3 py-2.5
                       text-sm text-slate-200 placeholder:text-slate-600 outline-none
                       focus:border-blue-500/40 focus:bg-white/[0.07] transition-colors duration-150
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
                ? 'bg-blue-600 hover:bg-blue-500 text-white shadow-glow'
                : 'bg-white/[0.05] text-slate-600 cursor-not-allowed',
            )}
            onClick={handleSend}
            disabled={!input.trim() || loading}
            aria-label="Send message"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
        <p className="mt-2 text-[10px] text-slate-600">
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
          ? 'bg-blue-600/20 ring-blue-500/30 text-blue-400'
          : 'bg-violet-500/15 ring-violet-500/25 text-violet-400',
      )}>
        {isUser
          ? <User className="h-3.5 w-3.5" />
          : <Bot className="h-3.5 w-3.5" />}
      </div>
      <div className={clsx('max-w-[82%] space-y-2', isUser && 'items-end flex flex-col')}>
        <div className={clsx(
          'rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed',
          isUser
            ? 'bg-blue-600/20 text-slate-200 rounded-tr-sm ring-1 ring-blue-500/20'
            : 'bg-white/[0.05] text-slate-300 rounded-tl-sm ring-1 ring-white/[0.07]',
        )}>
          {message.content}
        </div>
        {message.chart && (
          <div className="w-full glass rounded-xl p-3 ring-1 ring-white/[0.07]">
            <p className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-500">
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
      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-violet-500/15 ring-1 ring-violet-500/25">
        <Bot className="h-3.5 w-3.5 text-violet-400" />
      </div>
      <div className="flex items-center gap-1 rounded-2xl rounded-tl-sm bg-white/[0.05] px-4 py-3 ring-1 ring-white/[0.07]">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className="h-1.5 w-1.5 rounded-full bg-slate-500 animate-pulse"
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
        <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-500/10 ring-1 ring-violet-500/20">
          <Sparkles className="h-6 w-6 text-violet-400" />
        </div>
        <p className="text-sm font-medium text-slate-300">Ask anything about health data</p>
        <p className="mt-1 text-xs text-slate-500">WHO data across 5 East African countries</p>
      </div>
      <div className="space-y-2">
        {suggestions.map((s) => (
          <button key={s} className="w-full cursor-default rounded-xl bg-white/[0.03] px-3 py-2 text-left text-xs text-slate-500 ring-1 ring-white/[0.06]">
            {s}
          </button>
        ))}
      </div>
    </div>
  )
}
