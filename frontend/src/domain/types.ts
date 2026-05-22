export interface Coordinate {
  latitude: number
  longitude: number
}

export interface MicroSegmentMetadata {
  collected_at: string
  observations: string[]
  projection_horizon_weeks: number
}

export interface OperationalMicroSegment {
  id: string
  monitor_id?: string | null
  name: string
  road_name: string
  km_start: number
  km_end: number
  coordinates: Coordinate
  zone: string
  evi: number
  rain_forecast: number
  days_without_maintenance: number
  operational_risk: number
  contractual_weight: number
  maintenance_history_count: number
  operational_status: string
  ipo: number
  criticity_level: 'baixo' | 'moderado' | 'alto' | 'crítico'
  operational_recommendation: string
  recommended_intervention_deadline: string
  projected_priority_score_48h: number
  metadata: MicroSegmentMetadata
}

export interface MicroSegmentList {
  items: OperationalMicroSegment[]
  total: number
  skip: number
  limit: number
}

export interface SimulationProjectionRequest {
  horizon_weeks: number
  skip?: number
  limit?: number
}

export interface SimulationProjectionSummary {
  total_microsegments: number
  critical_count: number
  average_ipo: number
  average_future_priority_48h: number
}

export interface SimulationProjectionResponse {
  horizon_weeks: number
  items: OperationalMicroSegment[]
  summary: SimulationProjectionSummary
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
