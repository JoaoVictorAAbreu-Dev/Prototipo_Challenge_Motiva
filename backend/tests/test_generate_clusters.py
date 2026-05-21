import pytest

from app.application.use_cases.generate_clusters import (
    GenerateClustersMicroSegmentRequest,
    GenerateClustersRequest,
    GenerateClustersUseCase,
)
from app.domain.services.cluster_generation_service import ClusterGenerationService
from app.domain.services.logistics_compliance_buffer_service import (
    LogisticsComplianceBufferService,
)


@pytest.mark.anyio
async def test_generate_clusters_groups_nearby_critical_segments():
    use_case = GenerateClustersUseCase(
        ClusterGenerationService(),
        LogisticsComplianceBufferService(),
    )

    response = await use_case.execute(
        GenerateClustersRequest(
            microsegments=[
                GenerateClustersMicroSegmentRequest(
                    id="1",
                    name="Trecho Norte A",
                    latitude=-15.7901,
                    longitude=-47.8820,
                    priority_score=91,
                    projected_priority_score_48h=96,
                ),
                GenerateClustersMicroSegmentRequest(
                    id="2",
                    name="Trecho Norte B",
                    latitude=-15.7910,
                    longitude=-47.8808,
                    priority_score=88,
                    projected_priority_score_48h=94,
                ),
                GenerateClustersMicroSegmentRequest(
                    id="3",
                    name="Trecho Sul",
                    latitude=-15.9200,
                    longitude=-47.9900,
                    priority_score=82,
                    projected_priority_score_48h=83,
                ),
            ],
            epsilon_km=2,
            min_samples=2,
            minimum_priority_score=80,
        )
    )

    assert len(response) == 1
    cluster = response[0]
    assert cluster["priority_average"] >= 89
    assert len(cluster["microsegments"]) == 2
    assert cluster["km_total"] > 0
    assert cluster["fuel_saved_liters"] > 0
    assert cluster["logistics_compliance_buffer"]["hold_order"] is True
    assert (
        cluster["logistics_compliance_buffer"]["status_label"]
        == "ordem agrupada estrategicamente"
    )
