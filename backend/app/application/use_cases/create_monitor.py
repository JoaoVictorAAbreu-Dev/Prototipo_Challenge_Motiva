"""
Use Case: Create Monitor
Application layer - Business logic coordination
"""

from dataclasses import dataclass
from typing import Optional

from app.domain.entities.monitor import Monitor, MonitorType
from app.domain.value_objects import Coordinate, StatusEnum
from app.domain.repositories import MonitorRepository


@dataclass
class CreateMonitorRequest:
    """Request DTO for creating a monitor"""

    name: str
    description: str
    monitor_type: str
    latitude: float
    longitude: float
    radius_meters: Optional[float] = None


@dataclass
class CreateMonitorResponse:
    """Response DTO for monitor creation"""

    id: str
    name: str
    status: str
    created_at: str


class CreateMonitorUseCase:
    """Use case for creating a new monitor"""

    def __init__(self, repository: MonitorRepository):
        self.repository = repository

    async def execute(self, request: CreateMonitorRequest) -> CreateMonitorResponse:
        """Execute use case"""
        # Validate input
        monitor_type = MonitorType(request.monitor_type)
        coordinate = Coordinate(request.latitude, request.longitude)

        # Create entity
        import uuid

        monitor = Monitor(
            id=str(uuid.uuid4()),
            name=request.name,
            description=request.description,
            monitor_type=monitor_type,
            status=StatusEnum.ACTIVE,
            center_coordinate=coordinate,
            radius_meters=request.radius_meters,
        )

        # Persist
        saved_monitor = await self.repository.save(monitor)

        # Return response
        return CreateMonitorResponse(
            id=saved_monitor.id,
            name=saved_monitor.name,
            status=saved_monitor.status.value,
            created_at=saved_monitor.created_at.isoformat(),
        )
