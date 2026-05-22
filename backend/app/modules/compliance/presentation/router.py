from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from app.domain.exceptions import ResourceNotFoundError
from app.modules.compliance.application.use_cases import ExportComplianceReportUseCase
from app.modules.compliance.presentation.dependencies import (
    get_export_compliance_report_use_case,
)

router = APIRouter(tags=["compliance"])


@router.get("/export-compliance-report/{segment_id}")
async def export_compliance_report(
    segment_id: str,
    use_case: ExportComplianceReportUseCase = Depends(
        get_export_compliance_report_use_case
    ),
):
    try:
        result = await use_case.execute(segment_id)
        return Response(
            content=result.content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{result.filename}"'
            },
        )
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
