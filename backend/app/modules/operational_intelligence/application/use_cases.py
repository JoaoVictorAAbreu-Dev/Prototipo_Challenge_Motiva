from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import uuid

from app.domain.entities.ipo_assessment import IPOAssessment
from app.domain.entities.monitor import Monitor, MonitorType
from app.domain.exceptions import ResourceNotFoundError
from app.domain.repositories import MicroSegmentRepository, MonitorRepository
from app.domain.services.ipo_engine import IPOEngine
from app.domain.value_objects import (
    ContractualWeight,
    Coordinate,
    DaysWithoutMaintenance,
    Percentage,
    StatusEnum,
)
from app.modules.simulation.domain.services import SimulationProjectionService


@dataclass(frozen=True)
class CalculateIPORequest:
    evi: float
    rain_forecast: float
    days_without_maintenance: int
    operational_risk: float
    contractual_weight: int


@dataclass(frozen=True)
class CalculateIPOResponse:
    final_score: float
    criticity_level: str
    operational_recommendation: str
    recommended_intervention_deadline: str


class CalculateIPOUseCase:
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


@dataclass(frozen=True)
class CreateMonitorRequest:
    name: str
    description: str
    monitor_type: str
    latitude: float
    longitude: float
    radius_meters: Optional[float] = None


class CreateMonitorUseCase:
    def __init__(self, repository: MonitorRepository):
        self.repository = repository

    async def execute(self, request: CreateMonitorRequest) -> dict:
        monitor = Monitor(
            id=str(uuid.uuid4()),
            name=request.name,
            description=request.description,
            monitor_type=MonitorType(request.monitor_type),
            status=StatusEnum.ACTIVE,
            center_coordinate=Coordinate(request.latitude, request.longitude),
            radius_meters=request.radius_meters,
        )
        saved_monitor = await self.repository.save(monitor)
        return saved_monitor.to_dict()


class GetMonitorUseCase:
    def __init__(self, repository: MonitorRepository):
        self.repository = repository

    async def execute(self, monitor_id: str) -> dict:
        monitor = await self.repository.get_by_id(monitor_id)
        if monitor is None:
            raise ResourceNotFoundError("Monitor", monitor_id)
        return monitor.to_dict()


class ListMonitorsUseCase:
    def __init__(self, repository: MonitorRepository):
        self.repository = repository

    async def execute(self, skip: int = 0, limit: int = 20) -> dict:
        monitors = await self.repository.get_all(skip=skip, limit=limit)
        total = await self.repository.count()
        return {
            "items": [monitor.to_dict() for monitor in monitors],
            "total": total,
            "skip": skip,
            "limit": limit,
        }


class ListMicroSegmentsUseCase:
    def __init__(
        self,
        repository: MicroSegmentRepository,
        simulation_projection_service: SimulationProjectionService,
    ):
        self.repository = repository
        self.simulation_projection_service = simulation_projection_service

    async def execute(self, skip: int = 0, limit: int = 250) -> dict:
        items = await self.repository.get_all(skip=skip, limit=limit)
        total = await self.repository.count()
        return {
            "items": [
                self.simulation_projection_service.project(item, 0) for item in items
            ],
            "total": total,
            "skip": skip,
            "limit": limit,
        }


class GetMicroSegmentUseCase:
    def __init__(
        self,
        repository: MicroSegmentRepository,
        simulation_projection_service: SimulationProjectionService,
    ):
        self.repository = repository
        self.simulation_projection_service = simulation_projection_service

    async def execute(self, microsegment_id: str) -> dict | None:
        microsegment = await self.repository.get_by_id(microsegment_id)
        if microsegment is None:
            return None
        return self.simulation_projection_service.project(microsegment, 0)


__all__ = [
    "CalculateIPORequest",
    "CalculateIPOResponse",
    "CalculateIPOUseCase",
    "CreateMonitorRequest",
    "CreateMonitorUseCase",
    "GetMonitorUseCase",
    "ListMonitorsUseCase",
    "ListMicroSegmentsUseCase",
    "GetMicroSegmentUseCase",
]
