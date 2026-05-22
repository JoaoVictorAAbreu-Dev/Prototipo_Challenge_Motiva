from fastapi import APIRouter, Depends

from app.modules.simulation.application.use_cases import (
    ProjectSimulationRequest,
    ProjectSimulationUseCase,
)
from app.modules.simulation.presentation.dependencies import (
    get_project_simulation_use_case,
)
from app.presentation.schemas import (
    SimulationProjectionRequestSchema,
    SimulationProjectionResponseSchema,
)

router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.post("/project", response_model=SimulationProjectionResponseSchema)
async def project_simulation(
    schema: SimulationProjectionRequestSchema,
    use_case: ProjectSimulationUseCase = Depends(get_project_simulation_use_case),
):
    return await use_case.execute(
        ProjectSimulationRequest(
            horizon_weeks=schema.horizon_weeks,
            skip=schema.skip,
            limit=schema.limit,
        )
    )
