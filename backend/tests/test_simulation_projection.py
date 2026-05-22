from datetime import datetime

import pytest

from app.domain.entities.microsegment import MicroSegment
from app.domain.repositories import MicroSegmentRepository
from app.domain.services.ipo_engine import IPOEngine
from app.modules.simulation.application.use_cases import (
    ProjectSimulationRequest,
    ProjectSimulationUseCase,
)
from app.modules.simulation.domain.services import SimulationProjectionService


class InMemoryMicroSegmentRepository(MicroSegmentRepository):
    def __init__(self, items: list[MicroSegment]):
        self.items = items

    async def save_many(self, microsegments: list[MicroSegment]) -> None:
        self.items.extend(microsegments)

    async def get_by_id(self, microsegment_id: str):
        return next((item for item in self.items if item.id == microsegment_id), None)

    async def get_all(self, skip: int = 0, limit: int = 250):
        return self.items[skip : skip + limit]

    async def count(self) -> int:
        return len(self.items)


@pytest.mark.anyio
async def test_project_simulation_recalculates_operational_mesh():
    repository = InMemoryMicroSegmentRepository(
        [
            MicroSegment(
                id="MT-101",
                monitor_id=None,
                name="Microtrecho MT-101",
                road_name="BR-101 Trecho Monitorado",
                km_start=45.0,
                km_end=45.5,
                latitude=-12.75,
                longitude=-38.21,
                zone="critica",
                evi=71,
                rain_forecast=66,
                days_without_maintenance=80,
                operational_risk=79,
                contractual_weight=5,
                maintenance_history_count=9,
                operational_status="parcialmente_interditado",
                observations=["Vegetação densa e tendência de piora"],
                collected_at=datetime.utcnow(),
            )
        ]
    )
    use_case = ProjectSimulationUseCase(
        repository,
        SimulationProjectionService(IPOEngine()),
    )

    current_projection = await use_case.execute(ProjectSimulationRequest(horizon_weeks=0))
    future_projection = await use_case.execute(ProjectSimulationRequest(horizon_weeks=6))

    assert current_projection.items[0]["ipo"] > 0
    assert future_projection.items[0]["evi"] > current_projection.items[0]["evi"]
    assert future_projection.items[0]["ipo"] >= current_projection.items[0]["ipo"]
    assert future_projection.summary.total_microsegments == 1
