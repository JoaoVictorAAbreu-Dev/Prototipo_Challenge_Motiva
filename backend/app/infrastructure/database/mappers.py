"""
Mapper - Convert between domain entities and persistence models
"""

from app.domain.entities.monitor import Monitor, MonitorType
from app.domain.value_objects import Coordinate, StatusEnum
from app.infrastructure.database.models import MonitorModel


class MonitorMapper:
    """Maps Monitor domain entity to/from MonitorModel"""

    @staticmethod
    def to_domain(model: MonitorModel) -> Monitor:
        """Convert database model to domain entity"""
        longitude, latitude = _parse_point(model.center_point)
        coordinate = Coordinate(latitude=latitude, longitude=longitude)

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


def _parse_point(value) -> tuple[float, float]:
    if hasattr(value, "x") and hasattr(value, "y"):
        return float(value.x), float(value.y)

    if isinstance(value, str):
        normalized = value
        if normalized.startswith("SRID="):
            normalized = normalized.split(";", 1)[1]
        normalized = normalized.removeprefix("POINT(").removesuffix(")")
        longitude, latitude = normalized.split()
        return float(longitude), float(latitude)

    raise ValueError("Unsupported point geometry format")
