from datetime import datetime

import pytest

from app.domain.entities.microsegment import MicroSegment
from app.domain.repositories import MicroSegmentRepository
from app.domain.services.compliance_mirror_service import ComplianceMirrorService
from app.infrastructure.pdf.compliance_report_exporter import (
    ComplianceReportExporter,
)
from app.modules.compliance.application.use_cases import (
    ExportComplianceReportUseCase,
)


class InMemoryMicroSegmentRepository(MicroSegmentRepository):
    def __init__(self, microsegment: MicroSegment | None):
        self.microsegment = microsegment

    async def save_many(self, microsegments: list[MicroSegment]) -> None:
        if microsegments:
            self.microsegment = microsegments[0]

    async def get_by_id(self, microsegment_id: str):
        if self.microsegment and self.microsegment.id == microsegment_id:
            return self.microsegment
        return None

    async def get_all(self, skip: int = 0, limit: int = 20):
        return [self.microsegment] if self.microsegment else []

    async def count(self) -> int:
        return 1 if self.microsegment else 0


@pytest.mark.anyio
async def test_export_compliance_report_returns_pdf_bytes():
    microsegment = MicroSegment(
        id="segment-001",
        monitor_id=None,
        name="Trecho ANTT Norte",
        road_name="BR-101 Trecho Monitorado",
        km_start=3.0,
        km_end=3.5,
        latitude=-15.79,
        longitude=-47.88,
        zone="monitoramento",
        evi=57,
        rain_forecast=42,
        days_without_maintenance=31,
        operational_risk=46,
        contractual_weight=3,
        maintenance_history_count=6,
        operational_status="liberado",
        observations=["Trecho de evidência regulatória"],
        collected_at=datetime.utcnow(),
    )
    use_case = ExportComplianceReportUseCase(
        InMemoryMicroSegmentRepository(microsegment),
        ComplianceMirrorService(),
        ComplianceReportExporter(),
    )

    response = await use_case.execute("segment-001")

    assert response.filename == "compliance-report-segment-001.pdf"
    assert response.content.startswith(b"%PDF")
    assert len(response.content) > 1000


@pytest.mark.anyio
async def test_export_compliance_report_supports_operational_microsegment():
    microsegment = MicroSegment(
        id="MT-200",
        monitor_id=None,
        name="Microtrecho MT-200",
        road_name="BR-101 Trecho Monitorado",
        km_start=12.0,
        km_end=12.5,
        latitude=-12.8,
        longitude=-38.3,
        zone="critica",
        evi=81,
        rain_forecast=69,
        days_without_maintenance=95,
        operational_risk=88,
        contractual_weight=5,
        maintenance_history_count=13,
        operational_status="em_manutencao",
        observations=["Intervenção priorizada por degradação vegetal"],
        collected_at=datetime.utcnow(),
    )
    use_case = ExportComplianceReportUseCase(
        InMemoryMicroSegmentRepository(microsegment),
        ComplianceMirrorService(),
        ComplianceReportExporter(),
    )

    response = await use_case.execute("MT-200")

    assert response.filename == "compliance-report-MT-200.pdf"
    assert response.content.startswith(b"%PDF")
    assert len(response.content) > 1000
