"""
Logistics-compliance buffer decision engine
"""

from app.domain.entities.intervention_cluster import InterventionCluster
from app.domain.entities.logistics_compliance_buffer import (
    LogisticsComplianceDecision,
)


class LogisticsComplianceBufferService:
    """Evaluates whether an order should be held for logistical efficiency"""

    MAX_HOLD_HOURS = 48
    MIN_TREND_POINTS = 4.0
    MIN_COMPENSATION_SCORE = 3.0

    def evaluate(
        self,
        cluster: InterventionCluster,
        future_average_priority: float,
    ) -> LogisticsComplianceDecision:
        priority_delta = round(future_average_priority - cluster.average_priority, 2)
        compensation_score = round(
            priority_delta * 0.55
            + cluster.estimated_operational_savings * 6.5
            + cluster.estimated_fuel_saved_liters * 2.2
            + (cluster.optimized_time_minutes / 60) * 4.0,
            2,
        )

        should_hold = (
            priority_delta >= self.MIN_TREND_POINTS
            and compensation_score >= self.MIN_COMPENSATION_SCORE
        )

        if should_hold:
            return LogisticsComplianceDecision(
                hold_order=True,
                hold_hours=self.MAX_HOLD_HOURS,
                logistic_compensation_score=compensation_score,
                status_label="ordem agrupada estrategicamente",
                operational_justification=(
                    "Intervenção adiada por eficiência operacional: há cluster em "
                    "formação com tendência de aumento de criticidade nas próximas 48h."
                ),
            )

        return LogisticsComplianceDecision(
            hold_order=False,
            hold_hours=0,
            logistic_compensation_score=compensation_score,
            status_label="intervenção imediata recomendada",
            operational_justification=(
                "Execução liberada: o ganho logístico projetado não compensa reter "
                "a ordem de serviço."
            ),
        )
