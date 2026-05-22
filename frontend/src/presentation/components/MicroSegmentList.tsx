import { memo } from 'react'
import { OperationalMicroSegment } from '@/domain/types'
import { getCriticityColor } from '@/presentation/utils/operationalMap'

interface MicroSegmentListProps {
  loading?: boolean
  microsegments: OperationalMicroSegment[]
  onSelect?: (microsegment: OperationalMicroSegment) => void
  selectedId?: string
}

export const MicroSegmentList = memo<MicroSegmentListProps>(
  ({ microsegments, loading = false, onSelect, selectedId }) => {
    if (loading) {
      return (
        <div className="space-y-3">
          {[...Array(4)].map((_, index) => (
            <div
              key={index}
              className="h-28 animate-pulse rounded-2xl border border-white/8 bg-slate-900/80"
            />
          ))}
        </div>
      )
    }

    if (microsegments.length === 0) {
      return (
        <div className="flex items-center justify-center rounded-2xl border border-dashed border-white/10 bg-slate-950/60 py-12">
          <div className="text-center">
            <p className="text-slate-300">Nenhum microtrecho carregado</p>
            <p className="mt-1 text-sm text-slate-500">
              Verifique a malha operacional e o seed inicial
            </p>
          </div>
        </div>
      )
    }

    return (
      <div className="space-y-2.5">
        {microsegments.map((microsegment) => (
          <button
            key={microsegment.id}
            onClick={() => onSelect?.(microsegment)}
            className={`w-full rounded-2xl border p-4 text-left transition-all duration-200 ${
              selectedId === microsegment.id
                ? 'border-cyan-400/40 bg-cyan-400/8 shadow-[0_0_0_1px_rgba(34,211,238,0.12)]'
                : 'border-white/8 bg-slate-900/72 hover:border-cyan-400/18 hover:bg-slate-900/92'
            }`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span
                    className="h-2 w-2 rounded-full shadow-[0_0_10px_rgba(103,232,249,0.7)]"
                    style={{ background: getCriticityColor(microsegment.ipo) }}
                  />
                  <h3 className="truncate text-[15px] font-semibold tracking-[0.01em] text-white">
                    {microsegment.name}
                  </h3>
                </div>
                <p className="mt-2 line-clamp-2 text-sm leading-5 text-slate-400">
                  {microsegment.road_name} • km {microsegment.km_start.toFixed(1)}-
                  {microsegment.km_end.toFixed(1)} • {microsegment.zone}
                </p>
              </div>
              <span
                className="inline-flex shrink-0 rounded-full px-2.5 py-1 text-[11px] font-medium uppercase tracking-[0.18em]"
                style={{
                  backgroundColor: `${getCriticityColor(microsegment.ipo)}18`,
                  color: getCriticityColor(microsegment.ipo),
                }}
              >
                {microsegment.criticity_level}
              </span>
            </div>

            <div className="mt-4 grid grid-cols-3 gap-2 text-[11px] uppercase tracking-[0.16em] text-slate-500">
              <span>IPO {microsegment.ipo.toFixed(1)}</span>
              <span>EVI {microsegment.evi.toFixed(1)}</span>
              <span className="truncate text-right font-mono normal-case tracking-normal text-slate-400">
                {microsegment.coordinates.latitude.toFixed(4)},{' '}
                {microsegment.coordinates.longitude.toFixed(4)}
              </span>
            </div>
          </button>
        ))}
      </div>
    )
  },
)

MicroSegmentList.displayName = 'MicroSegmentList'
