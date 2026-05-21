"""
Use case: generate operational clusters
"""

from dataclasses import dataclass

from app.domain.entities.intervention_cluster import MicroSegment
from app.domain.services.cluster_generation_service import ClusterGenerationService
from app.domain.services.logistics_compliance_buffer_service import (
    LogisticsComplianceBufferService,
)


@dataclass(frozen=True)
class GenerateClustersMicroSegmentRequest:
    id: str
    name: str
    latitude: float
    longitude: float
    priority_score: float
    projected_priority_score_48h: float


@dataclass(frozen=True)
class GenerateClustersRequest:
    microsegments: list[GenerateClustersMicroSegmentRequest]
    epsilon_km: float = 8.0
    min_samples: int = 2
    minimum_priority_score: float = 75.0


class GenerateClustersUseCase:
    """Coordinates intervention cluster generation"""

    def __init__(
        self,
        cluster_generation_service: ClusterGenerationService,
        logistics_compliance_buffer_service: LogisticsComplianceBufferService,
    ):
        self.cluster_generation_service = cluster_generation_service
        self.logistics_compliance_buffer_service = logistics_compliance_buffer_service

    async def execute(self, request: GenerateClustersRequest) -> list[dict]:
        microsegments = [
            MicroSegment(
                id=item.id,
                name=item.name,
                latitude=item.latitude,
                longitude=item.longitude,
                priority_score=item.priority_score,
                projected_priority_score_48h=item.projected_priority_score_48h,
            )
            for item in request.microsegments
        ]

        clusters = self.cluster_generation_service.generate(
            microsegments=microsegments,
            epsilon_km=request.epsilon_km,
            min_samples=request.min_samples,
            minimum_priority_score=request.minimum_priority_score,
        )

        return [
            self._to_dict(cluster)
            for cluster in clusters
        ]

    def _to_dict(self, cluster) -> dict:
        future_average_priority = round(
            sum(
                segment.projected_priority_score_48h
                for segment in cluster.microsegments
            )
            / len(cluster.microsegments),
            2,
        )
        buffer_decision = self.logistics_compliance_buffer_service.evaluate(
            cluster=cluster,
            future_average_priority=future_average_priority,
        )

        return {
                "id": cluster.id,
                "centroid": {
                    "latitude": cluster.centroid_latitude,
                    "longitude": cluster.centroid_longitude,
                },
                "km_total": cluster.total_km,
                "priority_average": cluster.average_priority,
                "estimated_operational_savings": cluster.estimated_operational_savings,
                "fuel_saved_liters": cluster.estimated_fuel_saved_liters,
                "optimized_time_minutes": cluster.optimized_time_minutes,
                "future_priority_average_48h": future_average_priority,
                "logistics_compliance_buffer": {
                    "hold_order": buffer_decision.hold_order,
                    "hold_hours": buffer_decision.hold_hours,
                    "logistic_compensation_score": buffer_decision.logistic_compensation_score,
                    "status_label": buffer_decision.status_label,
                    "operational_justification": buffer_decision.operational_justification,
                },
                "microsegments": [
                    {
                        "id": segment.id,
                        "name": segment.name,
                        "latitude": segment.latitude,
                        "longitude": segment.longitude,
                        "priority_score": segment.priority_score,
                        "projected_priority_score_48h": segment.projected_priority_score_48h,
                    }
                    for segment in cluster.microsegments
                ],
            }
