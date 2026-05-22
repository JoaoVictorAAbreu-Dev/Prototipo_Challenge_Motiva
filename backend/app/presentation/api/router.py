"""
Top-level API router composition for the modular monolith
"""

from fastapi import APIRouter

from app.modules.compliance.presentation.router import router as compliance_router
from app.modules.logistics.presentation.router import router as logistics_router
from app.modules.operational_intelligence.presentation.router import (
    ipo_router,
    microsegment_router,
    router as operational_intelligence_router,
)
from app.modules.simulation.presentation.router import router as simulation_router

api_router = APIRouter()
api_router.include_router(operational_intelligence_router)
api_router.include_router(ipo_router)
api_router.include_router(microsegment_router)
api_router.include_router(logistics_router)
api_router.include_router(simulation_router)
api_router.include_router(compliance_router)
