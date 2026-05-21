import { Monitor } from '@/domain/types'

export type CriticityLevel = 'baixo' | 'moderado' | 'alto' | 'crítico'

export interface OperationalProjectionInput {
  simulatedWeeks?: number
}

export interface OperationalSegment {
  id: string
  monitor: Monitor
  ipo: number
  evi: number
  rainForecast: number
  operationalRisk: number
  daysWithoutMaintenance: number
  recommendation: string
  criticity: CriticityLevel
  color: string
  path: [number, number][]
  center: [number, number]
  heatRadius: number
  simulatedWeeks: number
  projectedIPO48h: number
}

export interface OperationalCluster {
  id: string
  segments: OperationalSegment[]
  center: [number, number]
  averageIPO: number
  color: string
}

const clamp = (value: number, min: number, max: number) =>
  Math.min(Math.max(value, min), max)

const hashSeed = (value: string): number =>
  value.split('').reduce((acc, char) => (acc * 31 + char.charCodeAt(0)) % 100000, 7)

const round = (value: number): number => Number(value.toFixed(1))

const resolveCriticity = (ipo: number): CriticityLevel => {
  if (ipo < 25) return 'baixo'
  if (ipo < 50) return 'moderado'
  if (ipo < 75) return 'alto'
  return 'crítico'
}

const resolveRecommendation = (criticity: CriticityLevel): string => {
  if (criticity === 'baixo') return 'Monitoramento contínuo e manutenção em janela padrão.'
  if (criticity === 'moderado') return 'Planejar manutenção preventiva e revisar impacto climático.'
  if (criticity === 'alto') return 'Priorizar equipe de campo e agir antes da próxima janela de chuva.'
  return 'Intervenção imediata com contingência operacional ativa.'
}

export const getCriticityColor = (ipo: number): string => {
  if (ipo < 25) return '#22c55e'
  if (ipo < 50) return '#f59e0b'
  if (ipo < 75) return '#f97316'
  return '#ef4444'
}

const buildPath = (
  latitude: number,
  longitude: number,
  seed: number,
  simulatedWeeks: number,
): [number, number][] => {
  const latSwing = ((seed % 17) + 8) / 6000
  const lngSwing = ((seed % 23) + 9) / 6000
  const diagonalBias = ((seed % 11) - 5) / 20000
  const driftFactor = simulatedWeeks / 12
  const latDrift = Math.sin(seed / 13 + driftFactor * 2.8) * 0.0024 * driftFactor
  const lngDrift = Math.cos(seed / 17 + driftFactor * 2.1) * 0.0032 * driftFactor

  return [
    [latitude - latSwing + latDrift * 0.8, longitude - lngSwing + lngDrift * 0.7],
    [latitude - latSwing / 3 + latDrift * 0.4, longitude - diagonalBias + lngDrift * 0.25],
    [latitude + latDrift * 0.2, longitude + lngSwing / 4 + lngDrift * 0.35],
    [latitude + latSwing / 2 + latDrift * 0.7, longitude + lngSwing + lngDrift * 0.8],
    [latitude + latSwing + latDrift, longitude + lngSwing / 2 + lngDrift],
  ]
}

const buildCenter = (
  latitude: number,
  longitude: number,
  seed: number,
  simulatedWeeks: number,
): [number, number] => {
  const driftFactor = simulatedWeeks / 12
  const latDrift = Math.sin(seed / 19 + driftFactor * 2.4) * 0.0065 * driftFactor
  const lngDrift = Math.cos(seed / 23 + driftFactor * 2.7) * 0.0075 * driftFactor
  return [latitude + latDrift, longitude + lngDrift]
}

export const buildOperationalSegments = (
  monitors: Monitor[],
  projection: OperationalProjectionInput = {},
): OperationalSegment[] => {
  const simulatedWeeks = projection.simulatedWeeks ?? 0

  return monitors.map((monitor) => {
    const seed = hashSeed(`${monitor.id}-${monitor.name}`)
    const baseLatitude = monitor.center_coordinate.latitude
    const baseLongitude = monitor.center_coordinate.longitude
    const center = buildCenter(baseLatitude, baseLongitude, seed, simulatedWeeks)

    const baseEvi = clamp(28 + (seed % 61), 0, 100)
    const baseRainForecast = clamp(20 + ((seed * 3) % 70), 0, 100)
    const baseDaysWithoutMaintenance = 5 + (seed % 120)
    const baseOperationalRisk = clamp(24 + ((seed * 5) % 72), 0, 100)
    const contractualWeight = 1 + (seed % 5)

    const eviIncrease = simulatedWeeks * (2.4 + (seed % 5) * 0.18)
    const rainIncrease = simulatedWeeks * (1.2 + (seed % 7) * 0.11)
    const riskIncrease = simulatedWeeks * (1.1 + (seed % 6) * 0.14)
    const maintenanceIncrease = simulatedWeeks * (4 + (seed % 4))

    const evi = round(clamp(baseEvi + eviIncrease, 0, 100))
    const rainForecast = round(clamp(baseRainForecast + rainIncrease, 0, 100))
    const operationalRisk = round(clamp(baseOperationalRisk + riskIncrease, 0, 100))
    const daysWithoutMaintenance = Math.round(
      clamp(baseDaysWithoutMaintenance + maintenanceIncrease, 0, 365),
    )
    const maintenanceFactor = clamp((daysWithoutMaintenance / 120) * 100, 0, 100)
    const ipo = round(
      evi * 0.3 +
        rainForecast * 0.15 +
        maintenanceFactor * 0.2 +
        operationalRisk * 0.2 +
        contractualWeight * 20 * 0.15,
    )
    const projectedPriorityScore48h = round(
      clamp(
        ipo + 0.3 * (1.8 + (seed % 5) * 0.2) + (rainForecast / 100) * 2.2,
        0,
        100,
      ),
    )
    const criticity = resolveCriticity(ipo)

    return {
      id: monitor.id,
      monitor,
      ipo,
      evi,
      rainForecast,
      operationalRisk,
      daysWithoutMaintenance,
      recommendation: resolveRecommendation(criticity),
      criticity,
      color: getCriticityColor(ipo),
      path: buildPath(baseLatitude, baseLongitude, seed, simulatedWeeks),
      center,
      heatRadius: 220 + (seed % 320) + simulatedWeeks * 14 + ipo * 0.65,
      simulatedWeeks,
      projectedIPO48h: projectedPriorityScore48h,
    }
  })
}

export const buildOperationalClusters = (
  segments: OperationalSegment[],
): OperationalCluster[] => {
  const clusters: OperationalCluster[] = []
  const visited = new Set<string>()

  segments.forEach((segment) => {
    if (visited.has(segment.id)) return

    const grouped = segments.filter((candidate) => {
      const distance =
        Math.abs(candidate.center[0] - segment.center[0]) +
        Math.abs(candidate.center[1] - segment.center[1])
      const dynamicThreshold =
        0.075 + ((segment.simulatedWeeks + candidate.simulatedWeeks) / 2) * 0.0024
      return distance <= dynamicThreshold
    })

    grouped.forEach((item) => visited.add(item.id))

    const center: [number, number] = [
      grouped.reduce((acc, item) => acc + item.center[0], 0) / grouped.length,
      grouped.reduce((acc, item) => acc + item.center[1], 0) / grouped.length,
    ]
    const averageIPO = round(
      grouped.reduce((acc, item) => acc + item.ipo, 0) / grouped.length,
    )

    clusters.push({
      id: `cluster-${segment.id}`,
      segments: grouped,
      center,
      averageIPO,
      color: getCriticityColor(averageIPO),
    })
  })

  return clusters
}

export const getOperationalSnapshot = (
  monitor: Monitor,
  projection: OperationalProjectionInput = {},
): OperationalSegment => buildOperationalSegments([monitor], projection)[0]
