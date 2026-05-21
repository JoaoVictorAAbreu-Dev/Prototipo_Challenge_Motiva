"""
API Routes - Monitor endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response

from app.presentation.schemas import (
    CalculateIPOResponseSchema,
    CalculateIPOSchema,
    CreateMonitorSchema,
    GenerateClustersSchema,
    InterventionClusterSchema,
    MonitorSchema,
    MonitorListSchema,
)
from app.presentation.dependencies import (
    get_calculate_ipo_use_case,
    get_create_monitor_use_case,
    get_export_compliance_report_use_case,
    get_generate_clusters_use_case,
    get_get_monitor_use_case,
    get_monitor_repository,
)
from app.application.use_cases.calculate_ipo import (
    CalculateIPORequest,
    CalculateIPOUseCase,
)
from app.application.use_cases.export_compliance_report import (
    ExportComplianceReportUseCase,
)
from app.application.use_cases.generate_clusters import (
    GenerateClustersMicroSegmentRequest,
    GenerateClustersRequest,
    GenerateClustersUseCase,
)
from app.application.use_cases.create_monitor import CreateMonitorUseCase
from app.application.use_cases.get_monitor import GetMonitorUseCase
from app.domain.exceptions import ResourceNotFoundError
from app.infrastructure.repositories.monitor_repository import (
    SQLAlchemyMonitorRepository,
)

router = APIRouter(prefix="/monitors", tags=["monitors"])
ipo_router = APIRouter(tags=["ipo"])
cluster_router = APIRouter(tags=["clusters"])
compliance_router = APIRouter(tags=["compliance"])


@router.post(
    "",
    response_model=MonitorSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new monitor",
)
async def create_monitor(
    schema: CreateMonitorSchema,
    use_case: CreateMonitorUseCase = Depends(get_create_monitor_use_case),
):
    """Create a new geospatial monitor"""
    try:
        response = await use_case.execute(
            {
                "name": schema.name,
                "description": schema.description,
                "monitor_type": schema.monitor_type,
                "latitude": schema.latitude,
                "longitude": schema.longitude,
                "radius_meters": schema.radius_meters,
            }
        )
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{monitor_id}",
    response_model=MonitorSchema,
    summary="Get a monitor by ID",
)
async def get_monitor(
    monitor_id: str,
    use_case: GetMonitorUseCase = Depends(get_get_monitor_use_case),
):
    """Retrieve a specific monitor"""
    try:
        response = await use_case.execute(monitor_id)
        return response
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "",
    response_model=MonitorListSchema,
    summary="List all monitors",
)
async def list_monitors(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    repository: SQLAlchemyMonitorRepository = Depends(get_monitor_repository),
):
    """List all monitors with pagination"""
    monitors = await repository.get_all(skip=skip, limit=limit)
    total = await repository.count()
    return {
        "items": [m.to_dict() for m in monitors],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@ipo_router.post(
    "/calculate-ipo",
    response_model=CalculateIPOResponseSchema,
    summary="Calculate operational priority score",
)
async def calculate_ipo(
    schema: CalculateIPOSchema,
    use_case: CalculateIPOUseCase = Depends(get_calculate_ipo_use_case),
):
    """Calculate IPO based on operational variables"""
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@cluster_router.post(
    "/generate-clusters",
    response_model=list[InterventionClusterSchema],
    summary="Generate intervention clusters from critical microsegments",
)
async def generate_clusters(
    schema: GenerateClustersSchema,
    use_case: GenerateClustersUseCase = Depends(get_generate_clusters_use_case),
):
    """Generate operational intervention clusters using DBSCAN"""
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
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@compliance_router.get(
    "/export-compliance-report/{segment_id}",
    summary="Export ANTT compliance dossier as PDF",
)
async def export_compliance_report(
    segment_id: str,
    use_case: ExportComplianceReportUseCase = Depends(
        get_export_compliance_report_use_case
    ),
):
    """Export a compliance evidence PDF for the given segment"""
    try:
        result = await use_case.execute(segment_id)
        return Response(
            content=result.content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{result.filename}"'
            },
        )
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
