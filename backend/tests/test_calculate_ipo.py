import pytest

from app.domain.services.ipo_engine import IPOEngine
from app.modules.operational_intelligence.application.use_cases import (
    CalculateIPORequest,
    CalculateIPOUseCase,
)


@pytest.mark.anyio
async def test_calculate_ipo_returns_critical_response():
    use_case = CalculateIPOUseCase(IPOEngine())

    response = await use_case.execute(
        CalculateIPORequest(
            evi=95,
            rain_forecast=90,
            days_without_maintenance=120,
            operational_risk=92,
            contractual_weight=5,
        )
    )

    assert response.criticity_level == "crítico"
    assert response.final_score >= 75
    assert response.recommended_intervention_deadline == "24 horas"
