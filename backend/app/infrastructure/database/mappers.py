"""
Mapper - Convert between domain entities and persistence models
"""

from shapely.geometry import Point
from app.domain.entities.monitor import Monitor, MonitorType
from app.domain.value_objects import Coordinate, StatusEnum
from app.infrastructure.database.models import MonitorModel


class MonitorMapper:
    """Maps Monitor domain entity to/from MonitorModel"""

    @staticmethod
    def to_domain(model: MonitorModel) -> Monitor:
        """Convert database model to domain entity"""
        # Extract coordinates from Point geometry
        coords = model.center_point.x, model.center_point.y
        coordinate = Coordinate(latitude=coords[1], longitude=coords[0])

        return Monitor(
            id=model.id,
            name=model.name,
            description=model.description,
            monitor_type=MonitorType(model.monitor_type),
            status=StatusEnum(model.status),
            center_coordinate=coordinate,
            radius_meters=model.radius_meters,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_persistence(entity: Monitor) -> MonitorModel:
        """Convert domain entity to database model"""
        # Create Point from coordinates (longitude, latitude for PostGIS)
        point = Point(entity.center_coordinate.longitude, entity.center_coordinate.latitude)

        return MonitorModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            monitor_type=entity.monitor_type.value,
            status=entity.status.value,
            center_point=f"SRID=4326;POINT({entity.center_coordinate.longitude} {entity.center_coordinate.latitude})",
            radius_meters=entity.radius_meters,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
