import { OperationalMicroSegment } from '@/domain/types'

export type CriticityLevel = 'baixo' | 'moderado' | 'alto' | 'crítico'

export interface OperationalSegmentVisual {
  id: string
  microsegment: OperationalMicroSegment
  path: [number, number][]
  center: [number, number]
  heatRadius: number
  color: string
}

const hashSeed = (value: string): number =>
  value
    .split('')
    .reduce((acc, char) => (acc * 31 + char.charCodeAt(0)) % 100000, 7)

export const getCriticityColor = (ipo: number): string => {
  if (ipo < 25) return '#22c55e'
  if (ipo < 50) return '#f59e0b'
  if (ipo < 75) return '#f97316'
  return '#ef4444'
}

export const buildOperationalVisuals = (
  microsegments: OperationalMicroSegment[],
): OperationalSegmentVisual[] =>
  microsegments.map((microsegment) => {
    const seed = hashSeed(`${microsegment.id}-${microsegment.zone}`)
    const baseLatitude = microsegment.coordinates.latitude
    const baseLongitude = microsegment.coordinates.longitude
    const kmSpan = Math.max(microsegment.km_end - microsegment.km_start, 0.2)
    const latDelta = kmSpan / 220
    const lngDelta = kmSpan / 215
    const bias = ((seed % 11) - 5) / 5000
    const path: [number, number][] = [
      [baseLatitude - latDelta * 0.7, baseLongitude - lngDelta * 0.8],
      [baseLatitude - latDelta * 0.25, baseLongitude - bias],
      [baseLatitude + latDelta * 0.15, baseLongitude + lngDelta * 0.2],
      [baseLatitude + latDelta * 0.6, baseLongitude + lngDelta * 0.85],
    ]

    return {
      id: microsegment.id,
      microsegment,
      center: [baseLatitude, baseLongitude],
      path,
      color: getCriticityColor(microsegment.ipo),
      heatRadius:
        180 + microsegment.ipo * 6 + microsegment.projected_priority_score_48h * 2,
    }
  })
