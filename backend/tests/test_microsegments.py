from datetime import datetime

import pytest

from app.domain.entities.microsegment import MicroSegment
from app.domain.repositories import MicroSegmentRepository
from app.modules.operational_intelligence.application.use_cases import (
    GetMicroSegmentUseCase,
    ListMicroSegmentsUseCase,
)
from app.modules.simulation.domain.services import SimulationProjectionService
from app.domain.services.ipo_engine import IPOEngine


class InMemoryMicroSegmentRepository(MicroSegmentRepository):
    def __init__(self, items: list[MicroSegment]):
        self.items = {item.id: item for item in items}

    async def save_many(self, microsegments: list[MicroSegment]) -> None:
        for item in microsegments:
            self.items[item.id] = item

    async def get_by_id(self, microsegment_id: str):
        return self.items.get(microsegment_id)

    async def get_all(self, skip: int = 0, limit: int = 250):
        values = sorted(self.items.values(), key=lambda item: item.km_start)
        return values[skip : skip + limit]

    async def count(self) -> int:
        return len(self.items)


def build_microsegment(segment_id: str, km_start: float) -> MicroSegment:
    return MicroSegment(
        id=segment_id,
        monitor_id=None,
        name=f"Microtrecho {segment_id}",
        road_name="BR-101 Trecho Monitorado",
        km_start=km_start,
        km_end=km_start + 0.5,
        latitude=-12.965 + km_start / 100,
        longitude=-38.510 + km_start / 100,
        zone="critica",
        evi=74,
        rain_forecast=68,
        days_without_maintenance=88,
        operational_risk=82,
        contractual_weight=5,
        maintenance_history_count=11,
        operational_status="em_manutencao",
        observations=["Faixa crítica sob observação"],
        collected_at=datetime.utcnow(),
    )


@pytest.mark.anyio
async def test_list_and_get_microsegments_returns_projected_mesh():
    repository = InMemoryMicroSegmentRepository(
        [build_microsegment("MT-001", 0), build_microsegment("MT-002", 0.5)]
    )
    projection_service = SimulationProjectionService(IPOEngine())

    list_use_case = ListMicroSegmentsUseCase(repository, projection_service)
    get_use_case = GetMicroSegmentUseCase(repository, projection_service)

    listing = await list_use_case.execute(skip=0, limit=10)
    detail = await get_use_case.execute("MT-001")

    assert listing["total"] == 2
    assert listing["items"][0]["ipo"] >= 0
    assert listing["items"][0]["coordinates"]["latitude"] < 0
    assert detail is not None
    assert detail["id"] == "MT-001"
    assert detail["criticity_level"] in {"alto", "crítico"}
