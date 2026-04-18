export default function LoadingSkeleton() {
  return (
    <div className="grid grid-cols-1 gap-5 xl:grid-cols-2">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="bg-white rounded-2xl p-5 shadow-glass border border-slate-200">
          <div className="space-y-3">
            <div className="h-4 w-2/3 animate-pulse rounded-lg bg-slate-200" />
            <div className="h-3 w-1/4 animate-pulse rounded-full bg-slate-100" />
          </div>
          <div className="mt-5 h-[220px] animate-pulse rounded-xl bg-slate-100" />
          <div className="mt-4 h-3 w-full animate-pulse rounded-lg bg-slate-100" />
        </div>
      ))}
    </div>
  )
}
