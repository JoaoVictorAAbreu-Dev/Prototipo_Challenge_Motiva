"""
Dependency Injection - FastAPI dependencies
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_session
from app.infrastructure.repositories.monitor_repository import (
    SQLAlchemyMonitorRepository,
)
from app.domain.services.cluster_generation_service import ClusterGenerationService
from app.domain.services.compliance_mirror_service import ComplianceMirrorService
from app.domain.services.logistics_compliance_buffer_service import (
    LogisticsComplianceBufferService,
)
from app.domain.services.ipo_engine import IPOEngine
from app.application.use_cases.generate_clusters import GenerateClustersUseCase
from app.application.use_cases.export_compliance_report import (
    ExportComplianceReportUseCase,
)
from app.application.use_cases.calculate_ipo import CalculateIPOUseCase
from app.application.use_cases.create_monitor import CreateMonitorUseCase
from app.application.use_cases.get_monitor import GetMonitorUseCase
from app.infrastructure.pdf.compliance_report_exporter import (
    ComplianceReportExporter,
)


async def get_monitor_repository(
    session: AsyncSession = Depends(get_session),
) -> SQLAlchemyMonitorRepository:
    """Get monitor repository instance"""
    return SQLAlchemyMonitorRepository(session)


async def get_create_monitor_use_case(
    repository: SQLAlchemyMonitorRepository = Depends(get_monitor_repository),
) -> CreateMonitorUseCase:
    """Get create monitor use case"""
    return CreateMonitorUseCase(repository)


async def get_get_monitor_use_case(
    repository: SQLAlchemyMonitorRepository = Depends(get_monitor_repository),
) -> GetMonitorUseCase:
    """Get monitor use case"""
    return GetMonitorUseCase(repository)


def get_ipo_engine() -> IPOEngine:
    """Get IPO engine domain service"""
    return IPOEngine()


def get_calculate_ipo_use_case(
    ipo_engine: IPOEngine = Depends(get_ipo_engine),
) -> CalculateIPOUseCase:
    """Get calculate IPO use case"""
    return CalculateIPOUseCase(ipo_engine)


def get_cluster_generation_service() -> ClusterGenerationService:
    """Get cluster generation domain service"""
    return ClusterGenerationService()


def get_compliance_mirror_service() -> ComplianceMirrorService:
    """Get compliance mirror domain service"""
    return ComplianceMirrorService()


def get_compliance_report_exporter() -> ComplianceReportExporter:
    """Get compliance PDF exporter"""
    return ComplianceReportExporter()


def get_logistics_compliance_buffer_service() -> LogisticsComplianceBufferService:
    """Get logistics buffer decision service"""
    return LogisticsComplianceBufferService()


def get_generate_clusters_use_case(
    cluster_generation_service: ClusterGenerationService = Depends(
        get_cluster_generation_service
    ),
    logistics_compliance_buffer_service: LogisticsComplianceBufferService = Depends(
        get_logistics_compliance_buffer_service
    ),
) -> GenerateClustersUseCase:
    """Get generate clusters use case"""
    return GenerateClustersUseCase(
        cluster_generation_service,
        logistics_compliance_buffer_service,
    )


async def get_export_compliance_report_use_case(
    repository: SQLAlchemyMonitorRepository = Depends(get_monitor_repository),
    compliance_mirror_service: ComplianceMirrorService = Depends(
        get_compliance_mirror_service
    ),
    compliance_report_exporter: ComplianceReportExporter = Depends(
        get_compliance_report_exporter
    ),
) -> ExportComplianceReportUseCase:
    """Get compliance export use case"""
    return ExportComplianceReportUseCase(
        repository,
        compliance_mirror_service,
        compliance_report_exporter,
    )
