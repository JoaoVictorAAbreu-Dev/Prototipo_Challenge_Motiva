from fastapi import Depends

from app.core.dependencies import (
    get_microsegment_repository,
    get_simulation_projection_service,
)
from app.domain.repositories import MicroSegmentRepository
from app.modules.simulation.application.use_cases import (
    ProjectSimulationUseCase,
)
from app.modules.simulation.domain.services import SimulationProjectionService


def get_project_simulation_use_case(
    repository: MicroSegmentRepository = Depends(get_microsegment_repository),
    simulation_projection_service: SimulationProjectionService = Depends(
        get_simulation_projection_service
    ),
) -> ProjectSimulationUseCase:
    return ProjectSimulationUseCase(repository, simulation_projection_service)
