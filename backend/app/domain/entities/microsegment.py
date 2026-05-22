"""
Operational microsegment entity.
"""

from __future__ import annotations

from datetime import datetime

from app.domain.entities.base import Entity


class MicroSegment(Entity):
    """Aggregate root for the operational digital twin mesh."""

    def __init__(
        self,
        id: str,
        name: str,
        road_name: str,
        km_start: float,
        km_end: float,
        latitude: float,
        longitude: float,
        zone: str,
        evi: float,
        rain_forecast: float,
        days_without_maintenance: int,
        operational_risk: float,
        contractual_weight: int,
        maintenance_history_count: int,
        operational_status: str,
        observations: list[str],
        collected_at: datetime,
        monitor_id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.name = name
        self.road_name = road_name
        self.km_start = km_start
        self.km_end = km_end
        self.latitude = latitude
        self.longitude = longitude
        self.zone = zone
        self.evi = evi
        self.rain_forecast = rain_forecast
        self.days_without_maintenance = days_without_maintenance
        self.operational_risk = operational_risk
        self.contractual_weight = contractual_weight
        self.maintenance_history_count = maintenance_history_count
        self.operational_status = operational_status
        self.observations = observations
        self.collected_at = collected_at
        self.monitor_id = monitor_id

