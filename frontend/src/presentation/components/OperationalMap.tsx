import { useEffect, useMemo, useRef } from 'react'
import L, { DivIcon, FeatureGroup, LayerGroup, Map as LeafletMap } from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { InterventionCluster, OperationalMicroSegment } from '@/domain/types'
import {
  buildOperationalVisuals,
  OperationalSegmentVisual,
} from '@/presentation/utils/operationalMap'

interface OperationalMapProps {
  className?: string
  interventionClusters?: InterventionCluster[]
  loading?: boolean
  microsegments?: OperationalMicroSegment[]
  onSegmentClick?: (microsegment: OperationalMicroSegment) => void
  simulatedWeeks?: number
  staleData?: boolean
}

const MAP_TILE_URL =
  import.meta.env.VITE_MAP_TILE_URL ||
  'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'

const createSegmentTooltip = (segment: OperationalSegmentVisual): string => `
  <div class="ops-tooltip">
    <div class="ops-tooltip__header">
      <div>
        <div class="ops-tooltip__eyebrow">Microtrecho inteligente</div>
        <div class="ops-tooltip__title">${segment.microsegment.name}</div>
      </div>
      <div class="ops-tooltip__badge" style="border-color:${segment.color};color:${segment.color};">
        IPO ${segment.microsegment.ipo.toFixed(1)}
      </div>
    </div>
    <div class="ops-tooltip__grid">
      <div><span>EVI</span><strong>${segment.microsegment.evi.toFixed(1)}</strong></div>
      <div><span>Risco operacional</span><strong>${segment.microsegment.operational_risk.toFixed(1)}</strong></div>
      <div><span>Dias sem manutenção</span><strong>${segment.microsegment.days_without_maintenance}</strong></div>
      <div><span>Nível</span><strong>${segment.microsegment.criticity_level}</strong></div>
    </div>
    <div class="ops-tooltip__footer">
      <span>Recomendação operacional</span>
      <strong>${segment.microsegment.operational_recommendation}</strong>
    </div>
  </div>
`

const createClusterTooltip = (cluster: InterventionCluster): string => `
  <div class="ops-tooltip">
    <div class="ops-tooltip__header">
      <div>
        <div class="ops-tooltip__eyebrow">Cluster de intervenção</div>
        <div class="ops-tooltip__title">${cluster.microsegments.length} microtrechos críticos</div>
      </div>
      <div class="ops-tooltip__badge" style="border-color:#38bdf8;color:#38bdf8;">
        IPO ${cluster.priority_average}
      </div>
    </div>
    <div class="ops-tooltip__grid">
      <div><span>KM total</span><strong>${cluster.km_total} km</strong></div>
      <div><span>Economia operacional</span><strong>${cluster.estimated_operational_savings} km</strong></div>
      <div><span>Combustível economizado</span><strong>${cluster.fuel_saved_liters} L</strong></div>
      <div><span>Tempo otimizado</span><strong>${cluster.optimized_time_minutes} min</strong></div>
    </div>
    <div class="ops-tooltip__footer">
      <span>${cluster.logistics_compliance_buffer.status_label}</span>
      <strong>${cluster.logistics_compliance_buffer.operational_justification}</strong>
    </div>
  </div>
`

export const OperationalMap = ({
  className = '',
  interventionClusters = [],
  loading = false,
  microsegments = [],
  onSegmentClick,
  simulatedWeeks = 0,
  staleData = false,
}: OperationalMapProps) => {
  const containerRef = useRef<HTMLDivElement>(null)
  const mapRef = useRef<LeafletMap | null>(null)
  const overlayGroupRef = useRef<LayerGroup | null>(null)
  const boundsSignatureRef = useRef<string | null>(null)
  const segmentData = useMemo(
    () => buildOperationalVisuals(microsegments),
    [microsegments],
  )

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return

    const map = L.map(containerRef.current, {
      zoomControl: false,
      attributionControl: false,
    }).setView([-12.965, -38.51], 10)

    L.tileLayer(MAP_TILE_URL, {
      attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
      maxZoom: 19,
    }).addTo(map)

    L.control.zoom({ position: 'bottomright' }).addTo(map)
    L.control
      .attribution({ position: 'bottomleft', prefix: false })
      .addAttribution('Nexus-SENTINEL Operational Surface')
      .addTo(map)

    overlayGroupRef.current = L.layerGroup().addTo(map)
    mapRef.current = map

    return () => {
      map.remove()
      mapRef.current = null
      overlayGroupRef.current = null
      boundsSignatureRef.current = null
    }
  }, [])

  useEffect(() => {
    const map = mapRef.current
    const overlayGroup = overlayGroupRef.current
    if (!map || !overlayGroup) return

    overlayGroup.clearLayers()
    if (segmentData.length === 0) return

    const boundsGroup = new FeatureGroup()

    segmentData.forEach((segment) => {
      const heatHalo = L.circle(segment.center, {
        radius: segment.heatRadius,
        color: segment.color,
        opacity: 0.1,
        fillColor: segment.color,
        fillOpacity: 0.08,
        weight: 1,
      })
      const heatCore = L.circle(segment.center, {
        radius: segment.heatRadius * 0.42,
        color: segment.color,
        opacity: 0.2,
        fillColor: segment.color,
        fillOpacity: 0.22,
        weight: 1,
      })
      const microSegmentLayer = L.polyline(segment.path, {
        color: segment.color,
        weight: 5,
        opacity: 0.96,
        lineCap: 'round',
        lineJoin: 'round',
      }).bindTooltip(createSegmentTooltip(segment), {
        className: 'ops-tooltip-shell',
        sticky: true,
        direction: 'top',
        offset: [0, -10],
      })
      const nodeMarker = L.circleMarker(segment.center, {
        radius: 7 + segment.microsegment.ipo / 20,
        color: '#dbe4ff',
        weight: 1,
        fillColor: segment.color,
        fillOpacity: 0.95,
      }).bindTooltip(createSegmentTooltip(segment), {
        className: 'ops-tooltip-shell',
        sticky: true,
        direction: 'top',
      })

      if (onSegmentClick) {
        microSegmentLayer.on('click', () => onSegmentClick(segment.microsegment))
        nodeMarker.on('click', () => onSegmentClick(segment.microsegment))
      }

      heatHalo.addTo(overlayGroup)
      heatCore.addTo(overlayGroup)
      microSegmentLayer.addTo(overlayGroup)
      nodeMarker.addTo(overlayGroup)
      boundsGroup.addLayer(microSegmentLayer)
      boundsGroup.addLayer(nodeMarker)
    })

    interventionClusters.forEach((cluster) => {
      const clusterCenter: [number, number] = [
        cluster.centroid.latitude,
        cluster.centroid.longitude,
      ]
      const clusterCircle = L.circle(clusterCenter, {
        radius: Math.max(cluster.km_total * 90, 420),
        color: '#38bdf8',
        opacity: 0.18,
        fillColor: '#0ea5e9',
        fillOpacity: 0.06,
        weight: 1.25,
        dashArray: '6 6',
      }).bindTooltip(createClusterTooltip(cluster), {
        className: 'ops-cluster-tooltip-shell',
        sticky: true,
        direction: 'right',
      })
      const marker = L.marker(clusterCenter, {
        icon: new DivIcon({
          className: 'ops-cluster-wrapper',
          html: `
            <div class="ops-cluster ops-cluster--dbscan" style="border-color:#38bdf8;box-shadow:0 0 0 10px rgba(8,47,73,.32);">
              <span class="ops-cluster__count">${cluster.microsegments.length}</span>
              <span class="ops-cluster__label">${cluster.km_total} km</span>
            </div>
          `,
          iconSize: [78, 78],
          iconAnchor: [39, 39],
        }),
      }).bindTooltip(createClusterTooltip(cluster), {
        className: 'ops-cluster-tooltip-shell',
        sticky: true,
        direction: 'right',
      })

      clusterCircle.addTo(overlayGroup)
      marker.addTo(overlayGroup)
      boundsGroup.addLayer(clusterCircle)
      boundsGroup.addLayer(marker)
    })

    const boundsSignature = segmentData.map((segment) => segment.id).join('|')
    if (boundsSignatureRef.current !== boundsSignature) {
      map.fitBounds(boundsGroup.getBounds(), {
        padding: [40, 40],
        maxZoom: 13,
      })
      boundsSignatureRef.current = boundsSignature
    }
  }, [interventionClusters, onSegmentClick, segmentData])

  return (
    <div className={`ops-map-shell ${className}`}>
      <div className="ops-map-shell__hud">
        <div>
          <p className="ops-map-shell__label">Operational surface</p>
          <h2 className="ops-map-shell__title">Nexus-SENTINEL Live Map</h2>
          <p className="ops-map-shell__pulse">
            Twin horizon {simulatedWeeks.toFixed(1)} semanas
          </p>
          {staleData && (
            <p className="mt-2 text-[11px] uppercase tracking-[0.18em] text-amber-300">
              exibindo última projeção válida
            </p>
          )}
        </div>
        <div className="ops-map-shell__legend">
          <span><i style={{ background: '#22c55e' }} />baixo</span>
          <span><i style={{ background: '#f59e0b' }} />moderado</span>
          <span><i style={{ background: '#f97316' }} />alto</span>
          <span><i style={{ background: '#ef4444' }} />crítico</span>
        </div>
      </div>
      {loading && (
        <div className="pointer-events-none absolute inset-x-6 top-24 z-[1000] rounded-2xl border border-cyan-400/15 bg-slate-950/80 px-4 py-3 text-sm text-cyan-100 backdrop-blur-md">
          Atualizando malha operacional e projeção temporal...
        </div>
      )}
      <div ref={containerRef} className="h-full w-full" />
    </div>
  )
}
