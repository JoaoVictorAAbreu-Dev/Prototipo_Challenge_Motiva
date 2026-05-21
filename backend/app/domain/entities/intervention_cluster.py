"""
Intervention cluster entities
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MicroSegment:
    """Operational microsegment used for clustering"""

    id: str
    name: str
    latitude: float
    longitude: float
    priority_score: float
    projected_priority_score_48h: float


@dataclass(frozen=True)
class InterventionCluster:
    """Cluster of nearby critical microsegments"""

    id: str
    centroid_latitude: float
    centroid_longitude: float
    microsegments: list[MicroSegment]
    total_km: float
    average_priority: float
    estimated_operational_savings: float
    estimated_fuel_saved_liters: float
    optimized_time_minutes: float
