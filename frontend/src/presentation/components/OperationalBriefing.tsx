import { memo } from 'react'
import { InterventionCluster, OperationalMicroSegment } from '@/domain/types'
import { getCriticityColor } from '@/presentation/utils/operationalMap'

interface OperationalBriefingProps {
  currentWeeks: number
  exportError: string | null
  exportingSegmentId: string | null
  onExport: () => void
  selectedCluster: InterventionCluster | null
  selectedSegment: OperationalMicroSegment | null
}

export const OperationalBriefing = memo<OperationalBriefingProps>(
  ({
    currentWeeks,
    exportError,
    exportingSegmentId,
    onExport,
    selectedCluster,
    selectedSegment,
  }) => {
    if (!selectedSegment) {
      return (
        <section className="flex min-h-[320px] items-center justify-center rounded-[24px] border border-dashed border-white/10 bg-slate-950/50 p-6 text-center text-sm text-slate-500">
          Selecione um microtrecho no mapa ou na lista para abrir o briefing
          operacional.
        </section>
      )
    }

    return (
      <section className="rounded-[24px] border border-white/10 bg-slate-950/70 p-5">
        <div className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <p className="text-[11px] uppercase tracking-[0.28em] text-slate-500">
              Operational briefing
            </p>
            <h3 className="mt-2 truncate text-xl font-semibold text-white">
              {selectedSegment.name}
            </h3>
          </div>
          <div
            className="rounded-full border px-3 py-1 text-sm font-semibold"
            style={{
              borderColor: `${getCriticityColor(selectedSegment.ipo)}55`,
              color: getCriticityColor(selectedSegment.ipo),
            }}
          >
            IPO {selectedSegment.ipo.toFixed(1)}
          </div>
        </div>

        <p className="mt-4 text-sm leading-6 text-slate-400">
          {selectedSegment.road_name} • km {selectedSegment.km_start.toFixed(1)}-
          {selectedSegment.km_end.toFixed(1)} • zona {selectedSegment.zone}
        </p>

        <div className="mt-4 grid grid-cols-2 gap-3">
          <MetricCard label="EVI" value={selectedSegment.evi.toFixed(1)} />
          <MetricCard
            label="Chuva projetada"
            value={selectedSegment.rain_forecast.toFixed(1)}
          />
          <MetricCard
            label="Risco operacional"
            value={selectedSegment.operational_risk.toFixed(1)}
          />
          <MetricCard
            label="Dias sem manutenção"
            value={String(selectedSegment.days_without_maintenance)}
          />
        </div>

        <div className="mt-4 rounded-2xl border border-cyan-400/10 bg-[#05111f] p-4">
          <p className="text-[11px] uppercase tracking-[0.24em] text-cyan-300/60">
            Recomendação
          </p>
          <p className="mt-2 text-sm leading-6 text-slate-300">
            {selectedSegment.operational_recommendation}
          </p>
        </div>

        {selectedCluster && (
          <div className="mt-4 rounded-2xl border border-amber-400/20 bg-amber-950/10 p-4">
            <p className="text-[11px] uppercase tracking-[0.24em] text-amber-200/70">
              {selectedCluster.logistics_compliance_buffer.status_label}
            </p>
            <p className="mt-2 text-sm leading-6 text-slate-300">
              {selectedCluster.logistics_compliance_buffer.operational_justification}
            </p>
            <div className="mt-3 grid grid-cols-1 gap-3 sm:grid-cols-2">
              <div className="rounded-xl border border-white/8 bg-slate-900/70 p-3 text-sm text-slate-300">
                cluster em formação
              </div>
              <div className="rounded-xl border border-white/8 bg-slate-900/70 p-3 text-sm text-slate-300">
                intervenção adiada por eficiência operacional
              </div>
            </div>
          </div>
        )}

        <div className="mt-4 rounded-2xl border border-fuchsia-400/10 bg-fuchsia-950/10 p-4">
          <p className="text-[11px] uppercase tracking-[0.24em] text-fuchsia-200/70">
            Estado temporal
          </p>
          <p className="mt-2 text-sm leading-6 text-slate-300">
            Projeção ativa em {currentWeeks.toFixed(1)} semanas com criticidade{' '}
            {selectedSegment.criticity_level}.
          </p>
        </div>

        <div className="mt-4 rounded-2xl border border-white/8 bg-slate-900/90 p-4">
          <p className="text-[11px] uppercase tracking-[0.24em] text-slate-500">
            Evidência operacional
          </p>
          <ul className="mt-2 space-y-2 text-sm text-slate-300">
            {selectedSegment.metadata.observations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="mt-4 rounded-2xl border border-white/8 bg-slate-900/90 p-4">
          <p className="text-[11px] uppercase tracking-[0.24em] text-slate-500">
            Posição
          </p>
          <p className="mt-2 font-mono text-sm text-slate-300">
            {selectedSegment.coordinates.latitude.toFixed(6)},{' '}
            {selectedSegment.coordinates.longitude.toFixed(6)}
          </p>
        </div>

        <div className="mt-4 grid grid-cols-1 gap-3">
          <button
            onClick={onExport}
            disabled={exportingSegmentId === selectedSegment.id}
            className="btn-primary w-full disabled:cursor-not-allowed disabled:opacity-60"
          >
            {exportingSegmentId === selectedSegment.id
              ? 'Exportando dossiê ANTT...'
              : 'Exportar dossiê de compliance'}
          </button>
          {exportError && (
            <div className="rounded-2xl border border-red-500/25 bg-red-950/30 px-4 py-3 text-sm text-red-200">
              {exportError}
            </div>
          )}
        </div>
      </section>
    )
  },
)

OperationalBriefing.displayName = 'OperationalBriefing'

const MetricCard = memo<{ label: string; value: string }>(({ label, value }) => (
  <div className="rounded-2xl border border-white/8 bg-slate-900/85 p-4">
    <p className="text-xs text-slate-500">{label}</p>
    <strong className="mt-2 block text-lg text-white">{value}</strong>
  </div>
))

MetricCard.displayName = 'MetricCard'
