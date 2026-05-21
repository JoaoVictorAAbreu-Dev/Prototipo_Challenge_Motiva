"""
Use case: export compliance report
"""

from dataclasses import dataclass

from app.domain.exceptions import ResourceNotFoundError
from app.domain.repositories import MonitorRepository
from app.domain.services.compliance_mirror_service import ComplianceMirrorService
from app.infrastructure.pdf.compliance_report_exporter import ComplianceReportExporter


@dataclass(frozen=True)
class ExportComplianceReportResponse:
    filename: str
    content: bytes


class ExportComplianceReportUseCase:
    """Coordinates ANTT evidence dossier generation"""

    def __init__(
        self,
        repository: MonitorRepository,
        compliance_mirror_service: ComplianceMirrorService,
        compliance_report_exporter: ComplianceReportExporter,
    ):
        self.repository = repository
        self.compliance_mirror_service = compliance_mirror_service
        self.compliance_report_exporter = compliance_report_exporter

    async def execute(self, segment_id: str) -> ExportComplianceReportResponse:
        monitor = await self.repository.get_by_id(segment_id)
        if not monitor:
            raise ResourceNotFoundError("Monitor", segment_id)

        report = self.compliance_mirror_service.build_report(monitor)
        pdf_content = self.compliance_report_exporter.export(report)

        return ExportComplianceReportResponse(
            filename=f"compliance-report-{segment_id}.pdf",
            content=pdf_content,
        )
