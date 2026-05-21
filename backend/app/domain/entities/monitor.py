"""
Monitor Entity - Domain entity for geospatial monitoring
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum

from app.domain.entities.base import Entity
from app.domain.value_objects import Coordinate, StatusEnum


class MonitorType(str, Enum):
    """Types of monitors"""

    PERIMETER = "perimeter"
    POINT = "point"
    POLYGON = "polygon"
    HEATMAP = "heatmap"


class Monitor(Entity):
    """
    Monitor Aggregate Root
    Represents a geospatial monitoring zone
    """

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        monitor_type: MonitorType,
        status: StatusEnum,
        center_coordinate: Coordinate,
        radius_meters: Optional[float] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        super().__init__(id, created_at, updated_at)
        self.name = name
        self.description = description
        self.monitor_type = monitor_type
        self.status = status
        self.center_coordinate = center_coordinate
        self.radius_meters = radius_meters

    def activate(self) -> None:
        """Activate the monitor"""
        if self.status != StatusEnum.INACTIVE:
            raise ValueError("Only inactive monitors can be activated")
        self.status = StatusEnum.ACTIVE
        self.update_timestamp()

    def deactivate(self) -> None:
        """Deactivate the monitor"""
        if self.status != StatusEnum.ACTIVE:
            raise ValueError("Only active monitors can be deactivated")
        self.status = StatusEnum.INACTIVE
        self.update_timestamp()

    def update_location(self, coordinate: Coordinate) -> None:
        """Update monitor location"""
        self.center_coordinate = coordinate
        self.update_timestamp()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "monitor_type": self.monitor_type.value,
            "status": self.status.value,
            "center_coordinate": self.center_coordinate.to_dict(),
            "radius_meters": self.radius_meters,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
