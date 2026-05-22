from fastapi import Depends

from app.core.dependencies import (
    get_ipo_engine,
    get_microsegment_repository,
    get_monitor_repository,
    get_simulation_projection_service,
)
from app.domain.repositories import MicroSegmentRepository, MonitorRepository
from app.domain.services.ipo_engine import IPOEngine
from app.modules.operational_intelligence.application.use_cases import (
    CalculateIPOUseCase,
    CreateMonitorUseCase,
    GetMicroSegmentUseCase,
    GetMonitorUseCase,
    ListMonitorsUseCase,
    ListMicroSegmentsUseCase,
)
from app.modules.simulation.domain.services import SimulationProjectionService


async def get_create_monitor_use_case(
    repository: MonitorRepository = Depends(get_monitor_repository),
) -> CreateMonitorUseCase:
    return CreateMonitorUseCase(repository)


async def get_get_monitor_use_case(
    repository: MonitorRepository = Depends(get_monitor_repository),
) -> GetMonitorUseCase:
    return GetMonitorUseCase(repository)


async def get_list_monitors_use_case(
    repository: MonitorRepository = Depends(get_monitor_repository),
) -> ListMonitorsUseCase:
    return ListMonitorsUseCase(repository)


def get_calculate_ipo_use_case(
    ipo_engine: IPOEngine = Depends(get_ipo_engine),
) -> CalculateIPOUseCase:
    return CalculateIPOUseCase(ipo_engine)


def get_list_microsegments_use_case(
    repository: MicroSegmentRepository = Depends(get_microsegment_repository),
    simulation_projection_service: SimulationProjectionService = Depends(
        get_simulation_projection_service
    ),
) -> ListMicroSegmentsUseCase:
    return ListMicroSegmentsUseCase(repository, simulation_projection_service)


def get_get_microsegment_use_case(
    repository: MicroSegmentRepository = Depends(get_microsegment_repository),
    simulation_projection_service: SimulationProjectionService = Depends(
        get_simulation_projection_service
    ),
) -> GetMicroSegmentUseCase:
    return GetMicroSegmentUseCase(repository, simulation_projection_service)
