from __future__ import annotations

from dataclasses import dataclass
import uuid

from app.domain.entities.ipo_assessment import IPOAssessment
from app.domain.entities.microsegment import MicroSegment
from app.domain.services.ipo_engine import IPOEngine
from app.domain.value_objects import ContractualWeight, DaysWithoutMaintenance, Percentage


@dataclass(frozen=True)
class SimulationProjectionService:
    ipo_engine: IPOEngine

    def project(self, microsegment: MicroSegment, horizon_weeks: float) -> dict:
        seasonal_seed = self._seed(microsegment.id)
        normalized_horizon = max(horizon_weeks, 0.0)
        evi = self._clamp(
            microsegment.evi + normalized_horizon * (1.7 + (seasonal_seed % 5) * 0.21),
            0,
            100,
        )
        rain_forecast = self._clamp(
            microsegment.rain_forecast
            + normalized_horizon * (0.95 + (seasonal_seed % 7) * 0.17),
            0,
            100,
        )
        operational_risk = self._clamp(
            microsegment.operational_risk
            + normalized_horizon * (1.15 + (seasonal_seed % 6) * 0.19),
            0,
            100,
        )
        days_without_maintenance = int(
            round(microsegment.days_without_maintenance + normalized_horizon * 7)
        )

        assessment = IPOAssessment(
            id=str(uuid.uuid4()),
            evi=Percentage(round(evi, 2)),
            rain_forecast=Percentage(round(rain_forecast, 2)),
            days_without_maintenance=DaysWithoutMaintenance(days_without_maintenance),
            operational_risk=Percentage(round(operational_risk, 2)),
            contractual_weight=ContractualWeight(microsegment.contractual_weight),
        )
        result = self.ipo_engine.calculate(assessment)
        projected_priority_score_48h = round(
            self._clamp(
                result.final_score
                + 1.2
                + (rain_forecast / 100) * 2.4
                + (operational_risk / 100) * 1.7,
                0,
                100,
            ),
            2,
        )
        return {
            "id": microsegment.id,
            "monitor_id": microsegment.monitor_id,
            "name": microsegment.name,
            "road_name": microsegment.road_name,
            "km_start": microsegment.km_start,
            "km_end": microsegment.km_end,
            "coordinates": {
                "latitude": round(microsegment.latitude, 6),
                "longitude": round(microsegment.longitude, 6),
            },
            "zone": microsegment.zone,
            "evi": round(evi, 2),
            "rain_forecast": round(rain_forecast, 2),
            "days_without_maintenance": days_without_maintenance,
            "operational_risk": round(operational_risk, 2),
            "contractual_weight": microsegment.contractual_weight,
            "maintenance_history_count": microsegment.maintenance_history_count,
            "operational_status": microsegment.operational_status,
            "ipo": round(result.final_score, 2),
            "criticity_level": result.criticity_level.value,
            "operational_recommendation": result.operational_recommendation,
            "recommended_intervention_deadline": result.recommended_intervention_deadline,
            "projected_priority_score_48h": projected_priority_score_48h,
            "metadata": {
                "collected_at": microsegment.collected_at.isoformat(),
                "observations": microsegment.observations,
                "projection_horizon_weeks": round(normalized_horizon, 1),
            },
        }

    def _seed(self, value: str) -> int:
        return sum((index + 1) * ord(char) for index, char in enumerate(value))

    def _clamp(self, value: float, minimum: float, maximum: float) -> float:
        return min(max(value, minimum), maximum)
