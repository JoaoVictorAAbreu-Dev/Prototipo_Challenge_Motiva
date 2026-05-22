from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.domain.exceptions import ResourceNotFoundError
from app.modules.operational_intelligence.application.use_cases import (
    CalculateIPORequest,
    CalculateIPOUseCase,
    CreateMonitorRequest,
    CreateMonitorUseCase,
    GetMicroSegmentUseCase,
    GetMonitorUseCase,
    ListMonitorsUseCase,
    ListMicroSegmentsUseCase,
)
from app.modules.operational_intelligence.presentation.dependencies import (
    get_calculate_ipo_use_case,
    get_create_monitor_use_case,
    get_get_microsegment_use_case,
    get_get_monitor_use_case,
    get_list_monitors_use_case,
    get_list_microsegments_use_case,
)
from app.presentation.schemas import (
    CalculateIPOResponseSchema,
    CalculateIPOSchema,
    CreateMonitorSchema,
    MicroSegmentListSchema,
    MicroSegmentSchema,
    MonitorListSchema,
    MonitorSchema,
)

router = APIRouter(prefix="/monitors", tags=["operational-intelligence"])
ipo_router = APIRouter(tags=["operational-intelligence"])


@router.post("", response_model=MonitorSchema, status_code=status.HTTP_201_CREATED)
async def create_monitor(
    schema: CreateMonitorSchema,
    use_case: CreateMonitorUseCase = Depends(get_create_monitor_use_case),
):
    try:
        return await use_case.execute(
            CreateMonitorRequest(
                name=schema.name,
                description=schema.description,
                monitor_type=schema.monitor_type,
                latitude=schema.latitude,
                longitude=schema.longitude,
                radius_meters=schema.radius_meters,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{monitor_id}", response_model=MonitorSchema)
async def get_monitor(
    monitor_id: str,
    use_case: GetMonitorUseCase = Depends(get_get_monitor_use_case),
):
    try:
        return await use_case.execute(monitor_id)
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("", response_model=MonitorListSchema)
async def list_monitors(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    use_case: ListMonitorsUseCase = Depends(get_list_monitors_use_case),
):
    return await use_case.execute(skip=skip, limit=limit)


@ipo_router.post("/calculate-ipo", response_model=CalculateIPOResponseSchema)
async def calculate_ipo(
    schema: CalculateIPOSchema,
    use_case: CalculateIPOUseCase = Depends(get_calculate_ipo_use_case),
):
    try:
        return await use_case.execute(
            CalculateIPORequest(
                evi=schema.evi,
                rain_forecast=schema.rain_forecast,
                days_without_maintenance=schema.days_without_maintenance,
                operational_risk=schema.operational_risk,
                contractual_weight=schema.contractual_weight,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


microsegment_router = APIRouter(tags=["operational-intelligence"])


@microsegment_router.get("/microsegments", response_model=MicroSegmentListSchema)
async def list_microsegments(
    skip: int = Query(0, ge=0),
    limit: int = Query(250, ge=1, le=500),
    use_case: ListMicroSegmentsUseCase = Depends(get_list_microsegments_use_case),
):
    return await use_case.execute(skip=skip, limit=limit)


@microsegment_router.get(
    "/microsegments/{microsegment_id}", response_model=MicroSegmentSchema
)
async def get_microsegment(
    microsegment_id: str,
    use_case: GetMicroSegmentUseCase = Depends(get_get_microsegment_use_case),
):
    result = await use_case.execute(microsegment_id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"MicroSegment '{microsegment_id}' not found",
        )
    return result
