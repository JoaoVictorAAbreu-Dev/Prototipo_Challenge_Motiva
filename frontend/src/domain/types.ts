// Frontend API types and interfaces - Domain layer

export interface Coordinate {
  latitude: number
  longitude: number
}

export interface Monitor {
  id: string
  name: string
  description: string
  monitor_type: 'perimeter' | 'point' | 'polygon' | 'heatmap'
  status: 'active' | 'inactive' | 'pending' | 'archived'
  center_coordinate: Coordinate
  radius_meters?: number
  created_at: string
  updated_at: string
}

export interface MonitorList {
  items: Monitor[]
  total: number
  skip: number
  limit: number
}

export interface CreateMonitorRequest {
  name: string
  description: string
  monitor_type: string
  latitude: number
  longitude: number
  radius_meters?: number
}

export interface ClusterGenerationMicrosegment {
  id: string
  name: string
  latitude: number
  longitude: number
  priority_score: number
  projected_priority_score_48h: number
}

export interface LogisticsComplianceBuffer {
  hold_order: boolean
  hold_hours: number
  logistic_compensation_score: number
  status_label: string
  operational_justification: string
}

export interface GenerateClustersRequest {
  microsegments: ClusterGenerationMicrosegment[]
  epsilon_km?: number
  min_samples?: number
  minimum_priority_score?: number
}

export interface InterventionCluster {
  id: string
  centroid: Coordinate
  km_total: number
  priority_average: number
  estimated_operational_savings: number
  fuel_saved_liters: number
  optimized_time_minutes: number
  future_priority_average_48h: number
  logistics_compliance_buffer: LogisticsComplianceBuffer
  microsegments: ClusterGenerationMicrosegment[]
}

export interface ApiError {
  detail: string
  error_code?: string
}
