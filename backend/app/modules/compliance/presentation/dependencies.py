from fastapi import Depends

from app.core.dependencies import get_microsegment_repository
from app.domain.services.compliance_mirror_service import ComplianceMirrorService
from app.infrastructure.pdf.compliance_report_exporter import (
    ComplianceReportExporter,
)
from app.modules.compliance.application.use_cases import ExportComplianceReportUseCase


def get_compliance_mirror_service() -> ComplianceMirrorService:
    return ComplianceMirrorService()


def get_compliance_report_exporter() -> ComplianceReportExporter:
    return ComplianceReportExporter()


async def get_export_compliance_report_use_case(
    repository=Depends(get_microsegment_repository),
    compliance_mirror_service: ComplianceMirrorService = Depends(
        get_compliance_mirror_service
    ),
    compliance_report_exporter: ComplianceReportExporter = Depends(
        get_compliance_report_exporter
    ),
) -> ExportComplianceReportUseCase:
    return ExportComplianceReportUseCase(
        repository,
        compliance_mirror_service,
        compliance_report_exporter,
    )
