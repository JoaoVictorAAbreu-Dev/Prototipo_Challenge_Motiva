from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.domain.repositories import MicroSegmentRepository, MonitorRepository
from app.domain.services.ipo_engine import IPOEngine
from app.infrastructure.repositories.microsegment_repository import (
    SQLAlchemyMicroSegmentRepository,
)
from app.infrastructure.repositories.monitor_repository import (
    SQLAlchemyMonitorRepository,
)
from app.modules.simulation.domain.services import SimulationProjectionService


async def get_monitor_repository(
    session: AsyncSession = Depends(get_session),
) -> MonitorRepository:
    return SQLAlchemyMonitorRepository(session)


async def get_microsegment_repository(
    session: AsyncSession = Depends(get_session),
) -> MicroSegmentRepository:
    return SQLAlchemyMicroSegmentRepository(session)


def get_ipo_engine() -> IPOEngine:
    return IPOEngine()


def get_simulation_projection_service(
    ipo_engine: IPOEngine = Depends(get_ipo_engine),
) -> SimulationProjectionService:
    return SimulationProjectionService(ipo_engine=ipo_engine)
