"""
IPO engine domain service
"""

from app.domain.entities.ipo_assessment import IPOAssessment
from app.domain.value_objects import CriticityLevel


class IPOEngine:
    """Calculates operational priority score and intervention guidance"""

    EVI_WEIGHT = 0.30
    RAIN_WEIGHT = 0.15
    MAINTENANCE_WEIGHT = 0.20
    OPERATIONAL_RISK_WEIGHT = 0.20
    CONTRACTUAL_WEIGHT = 0.15

    def calculate(self, assessment: IPOAssessment) -> IPOAssessment:
        score = (
            assessment.evi.normalized() * self.EVI_WEIGHT
            + assessment.rain_forecast.normalized() * self.RAIN_WEIGHT
            + assessment.days_without_maintenance.normalized()
            * self.MAINTENANCE_WEIGHT
            + assessment.operational_risk.normalized()
            * self.OPERATIONAL_RISK_WEIGHT
            + assessment.contractual_weight.normalized() * self.CONTRACTUAL_WEIGHT
        ) * 100

        criticity_level = self._resolve_criticity_level(score)
        recommendation, deadline = self._resolve_action_plan(criticity_level)

        assessment.register_result(
            final_score=score,
            criticity_level=criticity_level,
            operational_recommendation=recommendation,
            recommended_intervention_deadline=deadline,
        )
        return assessment

    def _resolve_criticity_level(self, score: float) -> CriticityLevel:
        if score < 25:
            return CriticityLevel.LOW
        if score < 50:
            return CriticityLevel.MODERATE
        if score < 75:
            return CriticityLevel.HIGH
        return CriticityLevel.CRITICAL

    def _resolve_action_plan(self, level: CriticityLevel) -> tuple[str, str]:
        if level == CriticityLevel.LOW:
            return "Manter monitoramento de rotina e acompanhar indicadores.", "30 dias"
        if level == CriticityLevel.MODERATE:
            return "Planejar intervenção preventiva e revisar janela de manutenção.", "14 dias"
        if level == CriticityLevel.HIGH:
            return "Priorizar equipe operacional e executar manutenção corretiva.", "7 dias"
        return (
            "Executar intervenção imediata e ativar contingência operacional.",
            "24 horas",
        )
