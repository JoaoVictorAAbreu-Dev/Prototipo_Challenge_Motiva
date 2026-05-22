from fastapi import Depends

from app.domain.services.cluster_generation_service import ClusterGenerationService
from app.domain.services.logistics_compliance_buffer_service import (
    LogisticsComplianceBufferService,
)
from app.modules.logistics.application.use_cases import GenerateClustersUseCase


def get_cluster_generation_service() -> ClusterGenerationService:
    return ClusterGenerationService()


def get_logistics_compliance_buffer_service() -> LogisticsComplianceBufferService:
    return LogisticsComplianceBufferService()


def get_generate_clusters_use_case(
    cluster_generation_service: ClusterGenerationService = Depends(
        get_cluster_generation_service
    ),
    logistics_compliance_buffer_service: LogisticsComplianceBufferService = Depends(
        get_logistics_compliance_buffer_service
    ),
) -> GenerateClustersUseCase:
    return GenerateClustersUseCase(
        cluster_generation_service,
        logistics_compliance_buffer_service,
    )
