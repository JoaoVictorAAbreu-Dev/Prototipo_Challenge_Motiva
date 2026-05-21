// Map Hook - Custom hook for Leaflet integration

import { useEffect, useRef } from 'react'
import L, { Map as LeafletMap } from 'leaflet'
import 'leaflet/dist/leaflet.css'

interface MapOptions {
  center?: [number, number]
  zoom?: number
  tileUrl?: string
}

export function useMap(
  containerRef: React.RefObject<HTMLDivElement>,
  options: MapOptions = {},
) {
  const mapRef = useRef<LeafletMap | null>(null)

  const {
    center = [-15.793889, -47.879444], // Brasília
    zoom = 13,
    tileUrl = import.meta.env.VITE_MAP_TILE_URL || 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  } = options

  useEffect(() => {
    if (!containerRef.current) return

    // Initialize map
    const map = L.map(containerRef.current).setView(center, zoom)

    L.tileLayer(tileUrl, {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 19,
    }).addTo(map)

    mapRef.current = map

    return () => {
      map.remove()
    }
  }, [center, zoom, tileUrl])

  return mapRef.current
}
