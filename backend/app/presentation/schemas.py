"""
Presentation Schemas - Request/Response DTOs for API
"""

from typing import Optional
from pydantic import BaseModel, Field


class CoordinateSchema(BaseModel):
    """Coordinate schema"""

    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")


class CreateMonitorSchema(BaseModel):
    """Schema for creating a monitor"""

    name: str = Field(..., min_length=1, max_length=255, description="Monitor name")
    description: str = Field(
        ..., min_length=1, max_length=1000, description="Monitor description"
    )
    monitor_type: str = Field(
        ..., description="Type of monitor (perimeter, point, polygon, heatmap)"
    )
    latitude: float = Field(..., ge=-90, le=90, description="Center latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Center longitude")
    radius_meters: Optional[float] = Field(None, description="Radius in meters")


class MonitorSchema(BaseModel):
    """Full monitor schema"""

    id: str
    name: str
    description: str
    monitor_type: str
    status: str
    center_coordinate: CoordinateSchema
    radius_meters: Optional[float]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class MonitorListSchema(BaseModel):
    """Paginated monitors list"""

    items: list[MonitorSchema]
    total: int
    skip: int
    limit: int


class ErrorSchema(BaseModel):
    """Error response schema"""

    detail: str
    error_code: Optional[str] = None


class CalculateIPOSchema(BaseModel):
    """Schema for IPO calculation input"""

    evi: float = Field(..., ge=0, le=100, description="EVI score from 0 to 100")
    rain_forecast: float = Field(
        ..., ge=0, le=100, description="Rain forecast severity from 0 to 100"
    )
    days_without_maintenance: int = Field(
        ..., ge=0, description="Days elapsed since last maintenance"
    )
    operational_risk: float = Field(
        ..., ge=0, le=100, description="Operational risk from 0 to 100"
    )
    contractual_weight: int = Field(
        ..., ge=1, le=5, description="Contractual weight from 1 to 5"
    )


class CalculateIPOResponseSchema(BaseModel):
    """Schema for IPO calculation output"""

    final_score: float
    criticity_level: str
    operational_recommendation: str
    recommended_intervention_deadline: str


class GenerateClustersMicroSegmentSchema(BaseModel):
    """Microsegment input for operational clustering"""

    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1, max_length=255)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    priority_score: float = Field(..., ge=0, le=100)
    projected_priority_score_48h: float = Field(..., ge=0, le=100)


class GenerateClustersSchema(BaseModel):
    """Schema for cluster generation"""

    microsegments: list[GenerateClustersMicroSegmentSchema] = Field(
        ..., min_length=1
    )
    epsilon_km: float = Field(8.0, gt=0, le=100)
    min_samples: int = Field(2, ge=1, le=50)
    minimum_priority_score: float = Field(75.0, ge=0, le=100)


class InterventionClusterMicroSegmentSchema(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    priority_score: float
    projected_priority_score_48h: float


class LogisticsComplianceBufferSchema(BaseModel):
    hold_order: bool
    hold_hours: int
    logistic_compensation_score: float
    status_label: str
    operational_justification: str


class InterventionClusterSchema(BaseModel):
    id: str
    centroid: CoordinateSchema
    km_total: float
    priority_average: float
    estimated_operational_savings: float
    fuel_saved_liters: float
    optimized_time_minutes: float
    future_priority_average_48h: float
    logistics_compliance_buffer: LogisticsComplianceBufferSchema
    microsegments: list[InterventionClusterMicroSegmentSchema]
