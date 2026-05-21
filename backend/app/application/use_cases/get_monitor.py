"""
Use Case: Get Monitor
Application layer - Business logic coordination
"""

from dataclasses import dataclass
from typing import Optional

from app.domain.repositories import MonitorRepository
from app.domain.exceptions import ResourceNotFoundError


@dataclass
class GetMonitorResponse:
    """Response DTO for getting a monitor"""

    id: str
    name: str
    description: str
    monitor_type: str
    status: str
    center_coordinate: dict
    radius_meters: Optional[float]
    created_at: str
    updated_at: str


class GetMonitorUseCase:
    """Use case for retrieving a monitor"""

    def __init__(self, repository: MonitorRepository):
        self.repository = repository

    async def execute(self, monitor_id: str) -> GetMonitorResponse:
        """Execute use case"""
        monitor = await self.repository.get_by_id(monitor_id)

        if not monitor:
            raise ResourceNotFoundError("Monitor", monitor_id)

        return GetMonitorResponse(
            id=monitor.id,
            name=monitor.name,
            description=monitor.description,
            monitor_type=monitor.monitor_type.value,
            status=monitor.status.value,
            center_coordinate=monitor.center_coordinate.to_dict(),
            radius_meters=monitor.radius_meters,
            created_at=monitor.created_at.isoformat(),
            updated_at=monitor.updated_at.isoformat(),
        )
