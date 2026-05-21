"""
IPO assessment entity
"""

from app.domain.entities.base import Entity
from app.domain.value_objects import (
    ContractualWeight,
    CriticityLevel,
    DaysWithoutMaintenance,
    Percentage,
)


class IPOAssessment(Entity):
    """Aggregate root for an operational priority evaluation"""

    def __init__(
        self,
        id: str,
        evi: Percentage,
        rain_forecast: Percentage,
        days_without_maintenance: DaysWithoutMaintenance,
        operational_risk: Percentage,
        contractual_weight: ContractualWeight,
    ):
        super().__init__(id=id)
        self.evi = evi
        self.rain_forecast = rain_forecast
        self.days_without_maintenance = days_without_maintenance
        self.operational_risk = operational_risk
        self.contractual_weight = contractual_weight
        self.final_score: float = 0.0
        self.criticity_level: CriticityLevel = CriticityLevel.LOW
        self.operational_recommendation: str = ""
        self.recommended_intervention_deadline: str = ""

    def register_result(
        self,
        final_score: float,
        criticity_level: CriticityLevel,
        operational_recommendation: str,
        recommended_intervention_deadline: str,
    ) -> None:
        self.final_score = round(final_score, 2)
        self.criticity_level = criticity_level
        self.operational_recommendation = operational_recommendation
        self.recommended_intervention_deadline = recommended_intervention_deadline
        self.update_timestamp()
