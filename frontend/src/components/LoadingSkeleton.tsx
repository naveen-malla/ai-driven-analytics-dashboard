export default function LoadingSkeleton() {
  return (
    <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="glass rounded-2xl p-5 shadow-glass">
          <div className="space-y-3">
            <div className="h-4 w-2/3 animate-pulse rounded-lg bg-white/[0.06]" />
            <div className="h-3 w-1/4 animate-pulse rounded-full bg-white/[0.04]" />
          </div>
          <div className="mt-5 h-[220px] animate-pulse rounded-xl bg-white/[0.04]" />
          <div className="mt-4 h-3 w-full animate-pulse rounded-lg bg-white/[0.04]" />
        </div>
      ))}
    </div>
  )
}
