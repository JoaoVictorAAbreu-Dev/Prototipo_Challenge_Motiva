import React, {
  startTransition,
  useDeferredValue,
  useEffect,
  useMemo,
  useState,
} from 'react'
import { MapComponent } from '@/presentation/components/MapComponent'
import { MonitorList } from '@/presentation/components/MonitorList'
import { useMonitorStore } from '@/application/stores/monitorStore'
import { InterventionCluster, Monitor } from '@/domain/types'
import { apiClient } from '@/infrastructure/api/client'
import {
  getCriticityColor,
  getOperationalSnapshot,
} from '@/presentation/utils/operationalMap'

interface ExecutiveMetric {
  title: string
  value: string
  note: string
  tone:
    | 'cyan'
    | 'blue'
    | 'emerald'
    | 'violet'
    | 'amber'
    | 'rose'
    | 'sky'
    | 'slate'
}

export const DashboardPage: React.FC = () => {
  const [selectedMonitor, setSelectedMonitor] = useState<Monitor | null>(null)
  const [targetWeeks, setTargetWeeks] = useState(0)
  const [simulatedWeeks, setSimulatedWeeks] = useState(0)
  const [interventionClusters, setInterventionClusters] = useState<
    InterventionCluster[]
  >([])
  const { monitors, loading, error, fetchMonitors } = useMonitorStore()
  const deferredWeeks = useDeferredValue(simulatedWeeks)

  const snapshots = useMemo(
    () =>
      monitors.map((monitor) =>
        getOperationalSnapshot(monitor, { simulatedWeeks: deferredWeeks }),
      ),
    [deferredWeeks, monitors],
  )

  const selectedSnapshot = selectedMonitor
    ? getOperationalSnapshot(selectedMonitor, { simulatedWeeks: deferredWeeks })
    : null

  const criticalCount = snapshots.filter((snapshot) => snapshot.ipo >= 75).length
  const averageIPOValue =
    snapshots.length > 0
      ? snapshots.reduce((acc, snapshot) => acc + snapshot.ipo, 0) /
        snapshots.length
      : 0
  const averageIPO = averageIPOValue.toFixed(1)
  const bufferedClusters = interventionClusters.filter(
    (cluster) => cluster.logistics_compliance_buffer.hold_order,
  )
  const totalLogisticSavingsValue = interventionClusters.reduce(
    (acc, cluster) => acc + cluster.estimated_operational_savings,
    0,
  )
  const totalFuelSavedValue = interventionClusters.reduce(
    (acc, cluster) => acc + cluster.fuel_saved_liters,
    0,
  )
  const teamsOptimized = Math.max(
    0,
    Math.ceil(
      interventionClusters.reduce(
        (acc, cluster) => acc + cluster.microsegments.length,
        0,
      ) / 3,
    ),
  )
  const averageFuturePriorityValue =
    interventionClusters.length > 0
      ? interventionClusters.reduce(
          (acc, cluster) => acc + cluster.future_priority_average_48h,
          0,
        ) / interventionClusters.length
      : 0
  const totalClusterDistance = interventionClusters.reduce(
    (acc, cluster) => acc + cluster.km_total,
    0,
  )
  const estimatedOperationalReductionValue =
    interventionClusters.length > 0 && totalClusterDistance > 0
      ? (totalLogisticSavingsValue / totalClusterDistance) * 100
      : 0
  const averageCompensationScoreValue =
    interventionClusters.length > 0
      ? interventionClusters.reduce(
          (acc, cluster) =>
            acc +
            cluster.logistics_compliance_buffer.logistic_compensation_score,
          0,
        ) / interventionClusters.length
      : 0
  const averageCriticityLabel =
    averageIPOValue >= 75
      ? 'crítica'
      : averageIPOValue >= 50
        ? 'alta'
        : averageIPOValue >= 25
          ? 'moderada'
          : 'baixa'
  const operationalForecast =
    averageFuturePriorityValue >= 85
      ? 'Escalada crítica em 48h'
      : averageFuturePriorityValue >= 70
        ? 'Pressão elevada em formação'
        : 'Janela estável sob observação'
  const operationalCompliance =
    interventionClusters.length > 0
      ? `${(
          (bufferedClusters.length / interventionClusters.length) *
          100
        ).toFixed(0)}% aderente`
      : 'Sem clusters'

  const selectedRelatedCluster =
    selectedMonitor == null
      ? null
      : interventionClusters.find((cluster) =>
          cluster.microsegments.some((segment) => segment.id === selectedMonitor.id),
        ) ?? null

  const executiveMetrics = useMemo<ExecutiveMetric[]>(
    () => [
      {
        title: 'redução operacional estimada',
        value: `${estimatedOperationalReductionValue.toFixed(1)}%`,
        note: 'deslocamento evitado por roteirização tática',
        tone: 'cyan',
      },
      {
        title: 'economia logística',
        value: `${totalLogisticSavingsValue.toFixed(1)} km`,
        note: 'malha consolidada em clusters de intervenção',
        tone: 'blue',
      },
      {
        title: 'combustível economizado',
        value: `${totalFuelSavedValue.toFixed(1)} L`,
        note: 'eficiência acumulada em campo',
        tone: 'emerald',
      },
      {
        title: 'equipes otimizadas',
        value: `${teamsOptimized}`,
        note: 'frentes racionalizadas por proximidade',
        tone: 'violet',
      },
      {
        title: 'clusters ativos',
        value: `${interventionClusters.length}`,
        note: `${bufferedClusters.length} com buffer estratégico`,
        tone: 'amber',
      },
      {
        title: 'criticidade média da malha',
        value: averageIPO,
        note: `faixa ${averageCriticityLabel}`,
        tone: 'rose',
      },
      {
        title: 'previsão operacional',
        value: averageFuturePriorityValue.toFixed(1),
        note: operationalForecast,
        tone: 'sky',
      },
      {
        title: 'conformidade operacional',
        value: operationalCompliance,
        note: `score logístico médio ${averageCompensationScoreValue.toFixed(1)}`,
        tone: 'slate',
      },
    ],
    [
      averageCompensationScoreValue,
      averageCriticityLabel,
      averageFuturePriorityValue,
      averageIPO,
      bufferedClusters.length,
      estimatedOperationalReductionValue,
      interventionClusters.length,
      operationalCompliance,
      operationalForecast,
      teamsOptimized,
      totalFuelSavedValue,
      totalLogisticSavingsValue,
    ],
  )

  useEffect(() => {
    fetchMonitors()
  }, [fetchMonitors])

  useEffect(() => {
    let frame = 0

    const animate = () => {
      setSimulatedWeeks((currentWeeks) => {
        const distance = targetWeeks - currentWeeks
        if (Math.abs(distance) < 0.05) return targetWeeks
        return currentWeeks + distance * 0.14
      })
      frame = window.requestAnimationFrame(animate)
    }

    frame = window.requestAnimationFrame(animate)
    return () => window.cancelAnimationFrame(frame)
  }, [targetWeeks])

  useEffect(() => {
    if (snapshots.length === 0) {
      setInterventionClusters([])
      return
    }

    const timeoutId = window.setTimeout(async () => {
      try {
        const clusters = await apiClient.generateClusters({
          microsegments: snapshots.map((snapshot) => ({
            id: snapshot.id,
            name: snapshot.monitor.name,
            latitude: snapshot.center[0],
            longitude: snapshot.center[1],
            priority_score: snapshot.ipo,
            projected_priority_score_48h: snapshot.projectedIPO48h,
          })),
          epsilon_km: 8,
          min_samples: 2,
          minimum_priority_score: 75,
        })
        setInterventionClusters(clusters)
      } catch {
        setInterventionClusters([])
      }
    }, 180)

    return () => window.clearTimeout(timeoutId)
  }, [snapshots])

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
          <button className="btn-primary shrink-0">+ Novo Monitor</button>
        </div>
      </header>

      <div className="mx-auto grid max-w-[1800px] grid-cols-1 gap-4 px-4 py-4 sm:px-6 lg:grid-cols-[300px_minmax(0,1fr)] lg:px-8 xl:grid-cols-[300px_minmax(0,1fr)_360px]">
        <aside className="space-y-4 lg:order-1">
          <section className="rounded-[24px] border border-cyan-400/10 bg-slate-950/70 p-5 shadow-[0_0_0_1px_rgba(34,211,238,0.04)]">
            <p className="text-[11px] uppercase tracking-[0.28em] text-cyan-300/60">
              Fleet summary
            </p>
            <div className="mt-4 grid grid-cols-2 gap-3">
              <div className="rounded-2xl border border-white/8 bg-slate-900/75 p-4">
                <p className="text-xs text-slate-500">Trechos</p>
                <strong className="mt-2 block text-2xl text-white">
                  {monitors.length}
                </strong>
              </div>
              <div className="rounded-2xl border border-white/8 bg-slate-900/75 p-4">
                <p className="text-xs text-slate-500">IPO médio</p>
                <strong className="mt-2 block text-2xl text-white">
                  {averageIPO}
                </strong>
              </div>
              <div className="rounded-2xl border border-white/8 bg-slate-900/75 p-4">
                <p className="text-xs text-slate-500">Críticos</p>
                <strong className="mt-2 block text-2xl text-[#f87171]">
                  {criticalCount}
                </strong>
              </div>
              <div className="rounded-2xl border border-white/8 bg-slate-900/75 p-4">
                <p className="text-xs text-slate-500">Buffer</p>
                <strong className="mt-2 block text-sm text-cyan-300">
                  {bufferedClusters.length} ordens retidas
                </strong>
              </div>
            </div>
          </section>

          {error && (
            <div className="rounded-2xl border border-red-500/25 bg-red-950/40 p-4 text-sm text-red-200">
              {error}
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
            <MonitorList
              monitors={monitors}
              loading={loading}
              selectedId={selectedMonitor?.id}
              onSelect={setSelectedMonitor}
            />
          </section>
        </aside>

        <main className="space-y-4 lg:order-2">
          <section className="executive-shell rounded-[28px] border border-white/10 p-5 sm:p-6">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div className="min-w-0">
                <p className="text-[10px] uppercase tracking-[0.38em] text-cyan-300/70">
                  Executive command layer
                </p>
                <h2 className="mt-2 text-2xl font-semibold tracking-tight text-white sm:text-[30px]">
                  Plataforma operacional de infraestrutura crítica
                </h2>
                <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
                  Superfície executiva para leitura de risco, agrupamento
                  logístico, intervenção temporal e conformidade operacional.
                </p>
              </div>
              <div className="rounded-full border border-cyan-400/15 bg-cyan-400/10 px-4 py-2 text-[11px] uppercase tracking-[0.22em] text-cyan-100">
                implantável • corporativo • industrial
              </div>
            </div>

            <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2 2xl:grid-cols-4">
              {executiveMetrics.map((metric) => (
                <div
                  key={metric.title}
                  className={`executive-kpi executive-kpi--${metric.tone}`}
                >
                  <span>{metric.title}</span>
                  <strong>{metric.value}</strong>
                  <small>{metric.note}</small>
                </div>
              ))}
            </div>

            <div className="mt-4 grid grid-cols-1 gap-3 xl:grid-cols-3">
              <div className="executive-note">
                <strong>Heatmap operacional</strong>
                <span>camadas térmicas reativas por criticidade e pressão de malha</span>
              </div>
              <div className="executive-note">
                <strong>Clusters de intervenção</strong>
                <span>DBSCAN consolidando ordens para elevar ROI logístico</span>
              </div>
              <div className="executive-note">
                <strong>Compliance Mirror</strong>
                <span>dossiês digitais exportáveis para trilha regulatória</span>
              </div>
            </div>
          </section>

          <section className="digital-twin-panel rounded-[24px] border border-cyan-400/10 bg-slate-950/70 p-5">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <p className="text-[11px] uppercase tracking-[0.24em] text-cyan-300/60">
                  Simulador temporal
                </p>
                <h3 className="mt-1 text-lg font-semibold text-white">
                  Simular próximas semanas
                </h3>
                <p className="mt-1 text-sm text-slate-400">
                  O Digital Twin projeta degradação de EVI, recalcula IPO e
                  reorganiza os clusters em tempo real.
                </p>
              </div>
              <div className="digital-twin-panel__counter">
                {deferredWeeks.toFixed(1)} sem
              </div>
            </div>

            <div className="mt-5 grid grid-cols-1 gap-3 xl:grid-cols-[minmax(0,1fr)_220px] xl:items-center">
              <input
                type="range"
                min={0}
                max={12}
                step={1}
                value={targetWeeks}
                onChange={(event) => {
                  const nextWeeks = Number(event.target.value)
                  startTransition(() => setTargetWeeks(nextWeeks))
                }}
                className="digital-twin-slider"
              />
              <div className="flex justify-between text-[11px] uppercase tracking-[0.2em] text-slate-500">
                <span>Agora</span>
                <span>12 semanas</span>
              </div>
            </div>
          </section>

          <section className="overflow-hidden rounded-[28px] border border-cyan-400/10 bg-slate-950/50 p-3 shadow-[0_20px_80px_rgba(2,6,23,0.55)]">
            <MapComponent
              monitors={monitors}
              interventionClusters={interventionClusters}
              onMonitorClick={setSelectedMonitor}
              className="h-[620px] xl:h-[760px]"
              simulatedWeeks={deferredWeeks}
            />
          </section>
        </main>

        <aside className="lg:order-3">
          {selectedMonitor && selectedSnapshot ? (
            <section className="rounded-[24px] border border-white/10 bg-slate-950/70 p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0">
                  <p className="text-[11px] uppercase tracking-[0.28em] text-slate-500">
                    Operational briefing
                  </p>
                  <h3 className="mt-2 truncate text-xl font-semibold text-white">
                    {selectedMonitor.name}
                  </h3>
                </div>
                <div
                  className="rounded-full border px-3 py-1 text-sm font-semibold"
                  style={{
                    borderColor: `${getCriticityColor(selectedSnapshot.ipo)}55`,
                    color: getCriticityColor(selectedSnapshot.ipo),
                  }}
                >
                  IPO {selectedSnapshot.ipo}
                </div>
              </div>

              <p className="mt-4 text-sm leading-6 text-slate-400">
                {selectedMonitor.description}
              </p>

              <div className="mt-4 grid grid-cols-2 gap-3">
                <div className="rounded-2xl border border-white/8 bg-slate-900/85 p-4">
                  <p className="text-xs text-slate-500">EVI</p>
                  <strong className="mt-2 block text-lg text-white">
                    {selectedSnapshot.evi}
                  </strong>
                </div>
                <div className="rounded-2xl border border-white/8 bg-slate-900/85 p-4">
                  <p className="text-xs text-slate-500">Chuva projetada</p>
                  <strong className="mt-2 block text-lg text-white">
                    {selectedSnapshot.rainForecast}
                  </strong>
                </div>
                <div className="rounded-2xl border border-white/8 bg-slate-900/85 p-4">
                  <p className="text-xs text-slate-500">Risco operacional</p>
                  <strong className="mt-2 block text-lg text-white">
                    {selectedSnapshot.operationalRisk}
                  </strong>
                </div>
                <div className="rounded-2xl border border-white/8 bg-slate-900/85 p-4">
                  <p className="text-xs text-slate-500">Dias sem manutenção</p>
                  <strong className="mt-2 block text-lg text-white">
                    {selectedSnapshot.daysWithoutMaintenance}
                  </strong>
                </div>
              </div>

              <div className="mt-4 rounded-2xl border border-cyan-400/10 bg-[#05111f] p-4">
                <p className="text-[11px] uppercase tracking-[0.24em] text-cyan-300/60">
                  Recomendação
                </p>
                <p className="mt-2 text-sm leading-6 text-slate-300">
                  {selectedSnapshot.recommendation}
                </p>
              </div>

              {selectedRelatedCluster && (
                <div className="mt-4 rounded-2xl border border-amber-400/20 bg-amber-950/10 p-4">
                  <p className="text-[11px] uppercase tracking-[0.24em] text-amber-200/70">
                    {selectedRelatedCluster.logistics_compliance_buffer.status_label}
                  </p>
                  <p className="mt-2 text-sm leading-6 text-slate-300">
                    {
                      selectedRelatedCluster.logistics_compliance_buffer
                        .operational_justification
                    }
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
                  Projeção ativa em {deferredWeeks.toFixed(1)} semanas com
                  criticidade {selectedSnapshot.criticity}.
                </p>
              </div>

              <div className="mt-4 rounded-2xl border border-white/8 bg-slate-900/90 p-4">
                <p className="text-[11px] uppercase tracking-[0.24em] text-slate-500">
                  Posição
                </p>
                <p className="mt-2 font-mono text-sm text-slate-300">
                  {selectedSnapshot.center[0].toFixed(6)},{' '}
                  {selectedSnapshot.center[1].toFixed(6)}
                </p>
              </div>
            </section>
          ) : (
            <section className="flex min-h-[320px] items-center justify-center rounded-[24px] border border-dashed border-white/10 bg-slate-950/50 p-6 text-center text-sm text-slate-500">
              Selecione um microtrecho no mapa ou na lista para abrir o briefing
              operacional.
            </section>
          )}
        </aside>
      </div>
    </div>
  )
}
