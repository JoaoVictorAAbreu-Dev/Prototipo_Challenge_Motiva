from datetime import datetime

import pytest

from app.application.use_cases.export_compliance_report import (
    ExportComplianceReportUseCase,
)
from app.domain.entities.monitor import Monitor, MonitorType
from app.domain.repositories import MonitorRepository
from app.domain.services.compliance_mirror_service import ComplianceMirrorService
from app.domain.value_objects import Coordinate, StatusEnum
from app.infrastructure.pdf.compliance_report_exporter import (
    ComplianceReportExporter,
)


class InMemoryMonitorRepository(MonitorRepository):
    def __init__(self, monitor: Monitor | None):
        self.monitor = monitor

    async def save(self, monitor: Monitor) -> Monitor:
        self.monitor = monitor
        return monitor

    async def get_by_id(self, monitor_id: str):
        if self.monitor and self.monitor.id == monitor_id:
            return self.monitor
        return None

    async def get_all(self, skip: int = 0, limit: int = 20):
        return [self.monitor] if self.monitor else []

    async def find_by_status(self, status: str, skip: int = 0, limit: int = 20):
        return []

    async def delete(self, monitor_id: str) -> bool:
        return False

    async def count(self) -> int:
        return 1 if self.monitor else 0


@pytest.mark.anyio
async def test_export_compliance_report_returns_pdf_bytes():
    monitor = Monitor(
        id="segment-001",
        name="Trecho ANTT Norte",
        description="Segmento de evidência regulatória",
        monitor_type=MonitorType.POINT,
        status=StatusEnum.ACTIVE,
        center_coordinate=Coordinate(latitude=-15.79, longitude=-47.88),
        radius_meters=500,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    use_case = ExportComplianceReportUseCase(
        InMemoryMonitorRepository(monitor),
        ComplianceMirrorService(),
        ComplianceReportExporter(),
    )

    response = await use_case.execute("segment-001")

    assert response.filename == "compliance-report-segment-001.pdf"
    assert response.content.startswith(b"%PDF")
    assert len(response.content) > 1000
