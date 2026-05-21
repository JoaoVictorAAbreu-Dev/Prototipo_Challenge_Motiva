"""
Use case: calculate IPO
"""

from dataclasses import dataclass
import uuid

from app.domain.entities.ipo_assessment import IPOAssessment
from app.domain.services.ipo_engine import IPOEngine
from app.domain.value_objects import (
    ContractualWeight,
    DaysWithoutMaintenance,
    Percentage,
)


@dataclass(frozen=True)
class CalculateIPORequest:
    """Request DTO for IPO calculation"""

    evi: float
    rain_forecast: float
    days_without_maintenance: int
    operational_risk: float
    contractual_weight: int


@dataclass(frozen=True)
class CalculateIPOResponse:
    """Response DTO for IPO calculation"""

    final_score: float
    criticity_level: str
    operational_recommendation: str
    recommended_intervention_deadline: str


class CalculateIPOUseCase:
    """Application coordinator for IPO engine execution"""

    def __init__(self, ipo_engine: IPOEngine):
        self.ipo_engine = ipo_engine

    async def execute(self, request: CalculateIPORequest) -> CalculateIPOResponse:
        assessment = IPOAssessment(
            id=str(uuid.uuid4()),
            evi=Percentage(request.evi),
            rain_forecast=Percentage(request.rain_forecast),
            days_without_maintenance=DaysWithoutMaintenance(
                request.days_without_maintenance
            ),
            operational_risk=Percentage(request.operational_risk),
            contractual_weight=ContractualWeight(request.contractual_weight),
        )

        result = self.ipo_engine.calculate(assessment)

        return CalculateIPOResponse(
            final_score=result.final_score,
            criticity_level=result.criticity_level.value,
            operational_recommendation=result.operational_recommendation,
            recommended_intervention_deadline=result.recommended_intervention_deadline,
        )
