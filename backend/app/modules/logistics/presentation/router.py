from fastapi import APIRouter, Depends, HTTPException

from app.modules.logistics.application.use_cases import (
    GenerateClustersMicroSegmentRequest,
    GenerateClustersRequest,
    GenerateClustersUseCase,
)
from app.modules.logistics.presentation.dependencies import (
    get_generate_clusters_use_case,
)
from app.presentation.schemas import (
    GenerateClustersSchema,
    InterventionClusterSchema,
)

router = APIRouter(tags=["logistics"])


@router.post("/generate-clusters", response_model=list[InterventionClusterSchema])
async def generate_clusters(
    schema: GenerateClustersSchema,
    use_case: GenerateClustersUseCase = Depends(get_generate_clusters_use_case),
):
    try:
        return await use_case.execute(
            GenerateClustersRequest(
                microsegments=[
                    GenerateClustersMicroSegmentRequest(
                        id=item.id,
                        name=item.name,
                        latitude=item.latitude,
                        longitude=item.longitude,
                        priority_score=item.priority_score,
                        projected_priority_score_48h=item.projected_priority_score_48h,
                    )
                    for item in schema.microsegments
                ],
                epsilon_km=schema.epsilon_km,
                min_samples=schema.min_samples,
                minimum_priority_score=schema.minimum_priority_score,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
