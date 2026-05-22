from dataclasses import dataclass

from app.domain.repositories import MicroSegmentRepository
from app.modules.simulation.application.dto import (
    SimulationProjectionResponse,
    SimulationProjectionSummary,
)
from app.modules.simulation.domain.services import SimulationProjectionService


@dataclass(frozen=True)
class ProjectSimulationRequest:
    horizon_weeks: float
    skip: int = 0
    limit: int = 250


class ProjectSimulationUseCase:
    def __init__(
        self,
        repository: MicroSegmentRepository,
        simulation_projection_service: SimulationProjectionService,
    ):
        self.repository = repository
        self.simulation_projection_service = simulation_projection_service

    async def execute(
        self, request: ProjectSimulationRequest
    ) -> SimulationProjectionResponse:
        microsegments = await self.repository.get_all(
            skip=request.skip,
            limit=request.limit,
        )
        projected_items = [
            self.simulation_projection_service.project(item, request.horizon_weeks)
            for item in microsegments
        ]
        total_items = len(projected_items)
        average_ipo = (
            round(sum(item["ipo"] for item in projected_items) / total_items, 2)
            if total_items
            else 0.0
        )
        average_future = (
            round(
                sum(item["projected_priority_score_48h"] for item in projected_items)
                / total_items,
                2,
            )
            if total_items
            else 0.0
        )
        critical_count = sum(
            1 for item in projected_items if item["criticity_level"] == "crítico"
        )
        return SimulationProjectionResponse(
            horizon_weeks=round(request.horizon_weeks, 1),
            items=projected_items,
            summary=SimulationProjectionSummary(
                total_microsegments=total_items,
                critical_count=critical_count,
                average_ipo=average_ipo,
                average_future_priority_48h=average_future,
            ),
        )
