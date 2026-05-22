import { startTransition } from 'react'
import { ExecutiveOverview } from '@/presentation/components/ExecutiveOverview'
import { MicroSegmentList } from '@/presentation/components/MicroSegmentList'
import { OperationalBriefing } from '@/presentation/components/OperationalBriefing'
import { OperationalMap } from '@/presentation/components/OperationalMap'
import { SimulationControl } from '@/presentation/components/SimulationControl'
import { useOperationalDashboard } from '@/presentation/hooks/useOperationalDashboard'

export const DashboardPage = () => {
  const {
    baseLoading,
    bufferedClusters,
    clusterError,
    clustersLoading,
    deferredWeeks,
    error,
    executiveMetrics,
    exportComplianceReport,
    exportError,
    exportingSegmentId,
    interventionClusters,
    microsegments,
    projection,
    projectionLoading,
    selectedRelatedCluster,
    selectedSnapshot,
    setSelectedSegment,
    setTargetWeeks,
    staleData,
    targetWeeks,
  } = useOperationalDashboard()

  return (
    <div className="min-h-screen bg-[#020617] text-slate-100">
      <header className="sticky top-0 z-20 border-b border-white/10 bg-[#06101f]/92 backdrop-blur-xl">
        <div className="mx-auto flex max-w-[1800px] items-center justify-between gap-6 px-4 py-4 sm:px-6 lg:px-8">
          <div className="min-w-0">
            <p className="text-[10px] uppercase tracking-[0.42em] text-cyan-300/70">
              Critical Infrastructure Platform
            </p>
            <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-2">
              <h1 className="text-2xl font-semibold tracking-tight text-white sm:text-[30px]">
                Nexus-SENTINEL
              </h1>
              <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-[11px] uppercase tracking-[0.22em] text-slate-300">
                command surface
              </span>
            </div>
            <p className="mt-2 max-w-2xl text-sm text-slate-400">
              Centro operacional para priorização de malha crítica, eficiência
              logística e conformidade regulatória.
            </p>
          </div>
          <button className="btn-primary shrink-0">Digital Twin ativo</button>
        </div>
      </header>

      <div className="mx-auto grid max-w-[1800px] grid-cols-1 gap-4 px-4 py-4 sm:px-6 lg:grid-cols-[300px_minmax(0,1fr)] lg:px-8 xl:grid-cols-[300px_minmax(0,1fr)_360px]">
        <aside className="space-y-4 lg:order-1">
          <section className="rounded-[24px] border border-cyan-400/10 bg-slate-950/70 p-5 shadow-[0_0_0_1px_rgba(34,211,238,0.04)]">
            <p className="text-[11px] uppercase tracking-[0.28em] text-cyan-300/60">
              Fleet summary
            </p>
            <div className="mt-4 grid grid-cols-2 gap-3">
              <SummaryCard
                label="Trechos"
                value={String(projection.summary.total_microsegments)}
              />
              <SummaryCard
                label="IPO médio"
                value={projection.summary.average_ipo.toFixed(1)}
              />
              <SummaryCard
                accent="text-[#f87171]"
                label="Críticos"
                value={String(projection.summary.critical_count)}
              />
              <SummaryCard
                accent="text-cyan-300 text-sm"
                label="Buffer"
                value={`${bufferedClusters.length} ordens retidas`}
              />
            </div>
          </section>

          {error && (
            <div className="rounded-2xl border border-red-500/25 bg-red-950/40 p-4 text-sm text-red-200">
              {error}
            </div>
          )}

          {staleData && (
            <div className="rounded-2xl border border-amber-500/25 bg-amber-950/35 p-4 text-sm text-amber-100">
              A última projeção válida foi mantida enquanto a API atualizava a
              malha.
            </div>
          )}

          {clusterError && (
            <div className="rounded-2xl border border-amber-500/20 bg-amber-950/20 p-4 text-sm text-amber-100">
              Clusters preservados do último ciclo válido. {clusterError}
            </div>
          )}

          <section className="rounded-[24px] border border-white/10 bg-slate-950/60 p-4">
            <div className="mb-4">
              <h2 className="text-base font-semibold text-white">
                Microtrechos inteligentes
              </h2>
              <p className="mt-1 text-sm text-slate-400">
                Selecione um trecho para abrir o quadro operacional.
              </p>
            </div>
            <MicroSegmentList
              microsegments={microsegments}
              loading={baseLoading || projectionLoading}
              selectedId={selectedSnapshot?.id}
              onSelect={setSelectedSegment}
            />
          </section>
        </aside>

        <main className="space-y-4 lg:order-2">
          <ExecutiveOverview metrics={executiveMetrics} />
          <SimulationControl
            currentWeeks={deferredWeeks}
            targetWeeks={targetWeeks}
            onChange={(value) => startTransition(() => setTargetWeeks(value))}
          />
          <section className="overflow-hidden rounded-[28px] border border-cyan-400/10 bg-slate-950/50 p-3 shadow-[0_20px_80px_rgba(2,6,23,0.55)]">
            <OperationalMap
              microsegments={microsegments}
              interventionClusters={interventionClusters}
              onSegmentClick={setSelectedSegment}
              className="h-[620px] xl:h-[760px]"
              simulatedWeeks={deferredWeeks}
              loading={projectionLoading || clustersLoading}
              staleData={staleData}
            />
          </section>
        </main>

        <aside className="lg:order-3">
          <OperationalBriefing
            currentWeeks={deferredWeeks}
            exportError={exportError}
            exportingSegmentId={exportingSegmentId}
            onExport={exportComplianceReport}
            selectedCluster={selectedRelatedCluster}
            selectedSegment={selectedSnapshot}
          />
        </aside>
      </div>
    </div>
  )
}

const SummaryCard = ({
  accent = 'text-white text-2xl',
  label,
  value,
}: {
  accent?: string
  label: string
  value: string
}) => (
  <div className="rounded-2xl border border-white/8 bg-slate-900/75 p-4">
    <p className="text-xs text-slate-500">{label}</p>
    <strong className={`mt-2 block ${accent}`}>{value}</strong>
  </div>
)
