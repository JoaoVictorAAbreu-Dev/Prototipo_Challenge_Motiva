"""
SQLAlchemy Repository Implementation - Monitor persistence
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.monitor import Monitor
from app.domain.repositories import MonitorRepository
from app.domain.value_objects import StatusEnum
from app.infrastructure.database.models import MonitorModel
from app.infrastructure.database.mappers import MonitorMapper


class SQLAlchemyMonitorRepository(MonitorRepository):
    """SQLAlchemy implementation of MonitorRepository"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, monitor: Monitor) -> Monitor:
        """Save a monitor"""
        model = MonitorMapper.to_persistence(monitor)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return MonitorMapper.to_domain(model)

    async def get_by_id(self, monitor_id: str) -> Optional[Monitor]:
        """Get monitor by ID"""
        query = select(MonitorModel).where(MonitorModel.id == monitor_id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return MonitorMapper.to_domain(model) if model else None

    async def get_all(self, skip: int = 0, limit: int = 20) -> List[Monitor]:
        """Get all monitors with pagination"""
        query = select(MonitorModel).offset(skip).limit(limit)
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [MonitorMapper.to_domain(model) for model in models]

    async def find_by_status(
        self, status: str, skip: int = 0, limit: int = 20
    ) -> List[Monitor]:
        """Find monitors by status"""
        query = (
            select(MonitorModel)
            .where(MonitorModel.status == status)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [MonitorMapper.to_domain(model) for model in models]

    async def delete(self, monitor_id: str) -> bool:
        """Delete a monitor"""
        query = select(MonitorModel).where(MonitorModel.id == monitor_id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if not model:
            return False
        await self.session.delete(model)
        await self.session.flush()
        return True

    async def count(self) -> int:
        """Count total monitors"""
        query = select(MonitorModel)
        result = await self.session.execute(query)
        return len(result.scalars().all())
