"""
SQLAlchemy repository for operational microsegments.
"""

from __future__ import annotations

from datetime import datetime
import json

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.microsegment import MicroSegment
from app.domain.repositories import MicroSegmentRepository
from app.infrastructure.database.models import MicroSegmentModel


class SQLAlchemyMicroSegmentRepository(MicroSegmentRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_many(self, microsegments: list[MicroSegment]) -> None:
        models = [
            MicroSegmentModel(
                id=item.id,
                monitor_id=item.monitor_id,
                name=item.name,
                road_name=item.road_name,
                km_start=item.km_start,
                km_end=item.km_end,
                latitude=item.latitude,
                longitude=item.longitude,
                zone=item.zone,
                evi=item.evi,
                rain_forecast=item.rain_forecast,
                days_without_maintenance=item.days_without_maintenance,
                operational_risk=item.operational_risk,
                contractual_weight=item.contractual_weight,
                maintenance_history_count=item.maintenance_history_count,
                operational_status=item.operational_status,
                observations=json.dumps(item.observations, ensure_ascii=False),
                collected_at=item.collected_at,
                location_point=(
                    f"SRID=4326;POINT({item.longitude} {item.latitude})"
                ),
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in microsegments
        ]
        self.session.add_all(models)
        await self.session.flush()

    async def get_by_id(self, microsegment_id: str) -> MicroSegment | None:
        result = await self.session.execute(
            select(MicroSegmentModel).where(MicroSegmentModel.id == microsegment_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def get_all(self, skip: int = 0, limit: int = 250) -> list[MicroSegment]:
        result = await self.session.execute(
            select(MicroSegmentModel)
            .order_by(MicroSegmentModel.km_start)
            .offset(skip)
            .limit(limit)
        )
        return [self._to_domain(model) for model in result.scalars().all()]

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(MicroSegmentModel)
        )
        return int(result.scalar_one())

    def _to_domain(self, model: MicroSegmentModel) -> MicroSegment:
        observations = json.loads(model.observations) if model.observations else []
        collected_at = model.collected_at or model.created_at or datetime.utcnow()
        return MicroSegment(
            id=model.id,
            monitor_id=model.monitor_id,
            name=model.name,
            road_name=model.road_name,
            km_start=model.km_start,
            km_end=model.km_end,
            latitude=model.latitude,
            longitude=model.longitude,
            zone=model.zone,
            evi=model.evi,
            rain_forecast=model.rain_forecast,
            days_without_maintenance=model.days_without_maintenance,
            operational_risk=model.operational_risk,
            contractual_weight=model.contractual_weight,
            maintenance_history_count=model.maintenance_history_count,
            operational_status=model.operational_status,
            observations=observations,
            collected_at=collected_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
