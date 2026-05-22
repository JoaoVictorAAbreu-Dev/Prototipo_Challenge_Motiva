from app.main import app


def test_public_routes_are_registered():
    paths = {route.path for route in app.routes}
    assert "/api/v1/microsegments" in paths
    assert "/api/v1/microsegments/{microsegment_id}" in paths
    assert "/api/v1/simulation/project" in paths
    assert "/api/v1/generate-clusters" in paths
    assert "/api/v1/export-compliance-report/{segment_id}" in paths
