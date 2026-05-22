from __future__ import annotations

from dataclasses import dataclass

from app.domain.exceptions import ResourceNotFoundError
from app.domain.repositories import MicroSegmentRepository
from app.domain.services.compliance_mirror_service import ComplianceMirrorService
from app.infrastructure.pdf.compliance_report_exporter import ComplianceReportExporter


@dataclass(frozen=True)
class ExportComplianceReportResponse:
    filename: str
    content: bytes


class ExportComplianceReportUseCase:
    def __init__(
        self,
        repository: MicroSegmentRepository,
        compliance_mirror_service: ComplianceMirrorService,
        compliance_report_exporter: ComplianceReportExporter,
    ):
        self.repository = repository
        self.compliance_mirror_service = compliance_mirror_service
        self.compliance_report_exporter = compliance_report_exporter

    async def execute(self, segment_id: str) -> ExportComplianceReportResponse:
        microsegment = await self.repository.get_by_id(segment_id)
        if microsegment is None:
            raise ResourceNotFoundError("MicroSegment", segment_id)

        report = self.compliance_mirror_service.build_report(microsegment)
        pdf_content = self.compliance_report_exporter.export(report)
        return ExportComplianceReportResponse(
            filename=f"compliance-report-{segment_id}.pdf",
            content=pdf_content,
        )


__all__ = ["ExportComplianceReportResponse", "ExportComplianceReportUseCase"]
