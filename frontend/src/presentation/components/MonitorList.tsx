import React from 'react'
import { Monitor } from '@/domain/types'

interface MonitorListProps {
  monitors: Monitor[]
  loading?: boolean
  onSelect?: (monitor: Monitor) => void
  selectedId?: string
}

export const MonitorList: React.FC<MonitorListProps> = ({
  monitors,
  loading = false,
  onSelect,
  selectedId,
}) => {
  if (loading) {
    return (
      <div className="space-y-3">
        {[...Array(4)].map((_, i) => (
          <div
            key={i}
            className="h-28 animate-pulse rounded-2xl border border-white/8 bg-slate-900/80"
          />
        ))}
      </div>
    )
  }

  if (monitors.length === 0) {
    return (
      <div className="flex items-center justify-center rounded-2xl border border-dashed border-white/10 bg-slate-950/60 py-12">
        <div className="text-center">
          <p className="text-slate-300">Nenhum monitor encontrado</p>
          <p className="mt-1 text-sm text-slate-500">
            Crie um novo monitor para começar
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-2.5">
      {monitors.map((monitor) => (
        <button
          key={monitor.id}
          onClick={() => onSelect?.(monitor)}
          className={`w-full rounded-2xl border p-4 text-left transition-all duration-200 ${
            selectedId === monitor.id
              ? 'border-cyan-400/40 bg-cyan-400/8 shadow-[0_0_0_1px_rgba(34,211,238,0.12)]'
              : 'border-white/8 bg-slate-900/72 hover:border-cyan-400/18 hover:bg-slate-900/92'
          }`}
        >
          <div className="flex items-start justify-between gap-3">
            <div className="min-w-0 flex-1">
              <div className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-cyan-300/90 shadow-[0_0_10px_rgba(103,232,249,0.7)]" />
                <h3 className="truncate text-[15px] font-semibold tracking-[0.01em] text-white">
                  {monitor.name}
                </h3>
              </div>
              <p className="mt-2 line-clamp-2 text-sm leading-5 text-slate-400">
                {monitor.description}
              </p>
            </div>
            <span
              className={`inline-flex shrink-0 rounded-full px-2.5 py-1 text-[11px] font-medium uppercase tracking-[0.18em] ${
                monitor.status === 'active'
                  ? 'bg-emerald-500/12 text-emerald-300'
                  : 'bg-slate-700/60 text-slate-300'
              }`}
            >
              {monitor.status}
            </span>
          </div>

          <div className="mt-4 grid grid-cols-[auto_1fr] items-center gap-3 text-[11px] uppercase tracking-[0.16em] text-slate-500">
            <span>{monitor.monitor_type}</span>
            <span className="truncate text-right font-mono normal-case tracking-normal text-slate-400">
              {monitor.center_coordinate.latitude.toFixed(4)},{' '}
              {monitor.center_coordinate.longitude.toFixed(4)}
            </span>
          </div>
        </button>
      ))}
    </div>
  )
}
