import { useDeferredValue, useEffect, useMemo, useRef, useState } from 'react'
import {
  InterventionCluster,
  OperationalMicroSegment,
  SimulationProjectionResponse,
} from '@/domain/types'
import { apiClient } from '@/infrastructure/api/client'
import { ExecutiveMetric } from '@/presentation/components/ExecutiveOverview'

const DEFAULT_PROJECTION: SimulationProjectionResponse = {
  horizon_weeks: 0,
  items: [],
  summary: {
    total_microsegments: 0,
    critical_count: 0,
    average_ipo: 0,
    average_future_priority_48h: 0,
  },
}

export const useOperationalDashboard = () => {
  const [selectedSegment, setSelectedSegment] =
    useState<OperationalMicroSegment | null>(null)
  const [targetWeeks, setTargetWeeks] = useState(0)
  const [simulatedWeeks, setSimulatedWeeks] = useState(0)
  const [projection, setProjection] =
    useState<SimulationProjectionResponse>(DEFAULT_PROJECTION)
  const [interventionClusters, setInterventionClusters] = useState<
    InterventionCluster[]
  >([])
  const [baseLoading, setBaseLoading] = useState(true)
  const [projectionLoading, setProjectionLoading] = useState(false)
  const [clustersLoading, setClustersLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [clusterError, setClusterError] = useState<string | null>(null)
  const [staleData, setStaleData] = useState(false)
  const [exportingSegmentId, setExportingSegmentId] = useState<string | null>(null)
  const [exportError, setExportError] = useState<string | null>(null)
  const projectionRequestIdRef = useRef(0)
  const clusterRequestIdRef = useRef(0)
  const deferredWeeks = useDeferredValue(simulatedWeeks)

  const microsegments = projection.items
  const selectedSnapshot = useMemo(
    () =>
      selectedSegment
        ? microsegments.find((item) => item.id === selectedSegment.id) ?? null
        : null,
    [microsegments, selectedSegment],
  )

  const selectedRelatedCluster = useMemo(
    () =>
      selectedSnapshot == null
        ? null
        : interventionClusters.find((cluster) =>
            cluster.microsegments.some(
              (segment) => segment.id === selectedSnapshot.id,
            ),
          ) ?? null,
    [interventionClusters, selectedSnapshot],
  )

  const bufferedClusters = useMemo(
    () =>
      interventionClusters.filter(
        (cluster) => cluster.logistics_compliance_buffer.hold_order,
      ),
    [interventionClusters],
  )

  const executiveMetrics = useMemo<ExecutiveMetric[]>(() => {
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
      projection.summary.average_ipo >= 75
        ? 'crítica'
        : projection.summary.average_ipo >= 50
          ? 'alta'
          : projection.summary.average_ipo >= 25
            ? 'moderada'
            : 'baixa'
    const operationalForecast =
      projection.summary.average_future_priority_48h >= 85
        ? 'Escalada crítica em 48h'
        : projection.summary.average_future_priority_48h >= 70
          ? 'Pressão elevada em formação'
          : 'Janela estável sob observação'
    const operationalCompliance =
      interventionClusters.length > 0
        ? `${(
            (bufferedClusters.length / interventionClusters.length) *
            100
          ).toFixed(0)}% aderente`
        : 'Sem clusters'

    return [
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
        value: projection.summary.average_ipo.toFixed(1),
        note: `faixa ${averageCriticityLabel}`,
        tone: 'rose',
      },
      {
        title: 'previsão operacional',
        value: projection.summary.average_future_priority_48h.toFixed(1),
        note: operationalForecast,
        tone: 'sky',
      },
      {
        title: 'conformidade operacional',
        value: operationalCompliance,
        note: `score logístico médio ${averageCompensationScoreValue.toFixed(1)}`,
        tone: 'slate',
      },
    ]
  }, [bufferedClusters.length, interventionClusters, projection.summary])

  useEffect(() => {
    let frame = 0

    const animate = () => {
      let shouldContinue = false
      setSimulatedWeeks((currentWeeks) => {
        const distance = targetWeeks - currentWeeks
        if (Math.abs(distance) < 0.05) {
          return targetWeeks
        }
        shouldContinue = true
        return currentWeeks + distance * 0.14
      })

      if (shouldContinue) {
        frame = window.requestAnimationFrame(animate)
      }
    }

    if (targetWeeks !== simulatedWeeks) {
      frame = window.requestAnimationFrame(animate)
    }

    return () => window.cancelAnimationFrame(frame)
  }, [simulatedWeeks, targetWeeks])

  useEffect(() => {
    let cancelled = false

    const loadInitialMesh = async () => {
      setBaseLoading(true)
      setError(null)
      try {
        const result = await apiClient.projectSimulation({ horizon_weeks: 0 })
        if (cancelled) return
        setProjection(result)
        setSelectedSegment(result.items[0] ?? null)
      } catch (requestError) {
        if (!cancelled) {
          setError(
            requestError instanceof Error
              ? requestError.message
              : 'Falha ao carregar a malha operacional',
          )
        }
      } finally {
        if (!cancelled) {
          setBaseLoading(false)
        }
      }
    }

    loadInitialMesh()
    return () => {
      cancelled = true
    }
  }, [])

  useEffect(() => {
    if (baseLoading) return
    let cancelled = false

    const timeoutId = window.setTimeout(async () => {
      setProjectionLoading(true)
      setError(null)
      const requestId = ++projectionRequestIdRef.current

      try {
        const result = await apiClient.projectSimulation({
          horizon_weeks: Number(deferredWeeks.toFixed(1)),
        })
        if (cancelled || requestId !== projectionRequestIdRef.current) return

        setProjection(result)
        setSelectedSegment((current) =>
          current
            ? result.items.find((item) => item.id === current.id) ??
              result.items[0] ??
              null
            : result.items[0] ?? null,
        )
        setStaleData(false)
      } catch (requestError) {
        if (!cancelled && requestId === projectionRequestIdRef.current) {
          setError(
            requestError instanceof Error
              ? requestError.message
              : 'Falha ao projetar o Digital Twin',
          )
          setStaleData(true)
        }
      } finally {
        if (!cancelled && requestId === projectionRequestIdRef.current) {
          setProjectionLoading(false)
        }
      }
    }, 160)

    return () => {
      cancelled = true
      window.clearTimeout(timeoutId)
    }
  }, [baseLoading, deferredWeeks])

  useEffect(() => {
    if (microsegments.length === 0) {
      setInterventionClusters([])
      setClusterError(null)
      return
    }

    let cancelled = false
    const timeoutId = window.setTimeout(async () => {
      setClustersLoading(true)
      const requestId = ++clusterRequestIdRef.current

      try {
        const clusters = await apiClient.generateClusters({
          microsegments: microsegments.map((segment) => ({
            id: segment.id,
            name: segment.name,
            latitude: segment.coordinates.latitude,
            longitude: segment.coordinates.longitude,
            priority_score: segment.ipo,
            projected_priority_score_48h: segment.projected_priority_score_48h,
          })),
          epsilon_km: 8,
          min_samples: 2,
          minimum_priority_score: 75,
        })
        if (cancelled || requestId !== clusterRequestIdRef.current) return

        setInterventionClusters(clusters)
        setClusterError(null)
      } catch (requestError) {
        if (cancelled || requestId !== clusterRequestIdRef.current) return

        setClusterError(
          requestError instanceof Error
            ? requestError.message
            : 'Falha ao atualizar clusters operacionais',
        )
      } finally {
        if (!cancelled && requestId === clusterRequestIdRef.current) {
          setClustersLoading(false)
        }
      }
    }, 180)

    return () => {
      cancelled = true
      window.clearTimeout(timeoutId)
    }
  }, [microsegments])

  const exportComplianceReport = async () => {
    if (!selectedSnapshot) return

    setExportingSegmentId(selectedSnapshot.id)
    setExportError(null)

    try {
      const blob = await apiClient.exportComplianceReport(selectedSnapshot.id)
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `compliance-report-${selectedSnapshot.id}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (requestError) {
      setExportError(
        requestError instanceof Error
          ? requestError.message
          : 'Falha ao exportar dossiê de compliance',
      )
    } finally {
      setExportingSegmentId(null)
    }
  }

  return {
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
    selectedSegment,
    selectedSnapshot,
    setSelectedSegment,
    setTargetWeeks,
    staleData,
    targetWeeks,
  }
}
