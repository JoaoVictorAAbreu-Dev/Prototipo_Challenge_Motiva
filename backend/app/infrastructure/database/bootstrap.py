"""
Database bootstrap and seed helpers.
"""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.domain.entities.microsegment import MicroSegment
from app.infrastructure.database.models import MicroSegmentModel
from app.infrastructure.repositories.microsegment_repository import (
    SQLAlchemyMicroSegmentRepository,
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[4]


def _seed_file() -> Path:
    return _project_root() / "highway_data.json"


async def seed_microsegments_if_empty(
    session_factory: async_sessionmaker,
) -> None:
    seed_path = _seed_file()
    if not seed_path.exists():
        return

    async with session_factory() as session:
        result = await session.execute(select(MicroSegmentModel.id).limit(1))
        if result.first():
            return

        payload = json.loads(seed_path.read_text(encoding="utf-8"))
        road_name = payload.get("rodovia", {}).get("nome", "Malha operacional")
        repository = SQLAlchemyMicroSegmentRepository(session)
        microsegments = [
            MicroSegment(
                id=item["id"],
                name=f"Microtrecho {item['id']}",
                road_name=road_name,
                km_start=float(item["km_inicial"]),
                km_end=float(item["km_final"]),
                latitude=float(item["latitude"]),
                longitude=float(item["longitude"]),
                zone=item["zona"],
                evi=round(float(item["valor_evi"]) * 100, 2),
                rain_forecast=float(item["previsao_chuva"]),
                days_without_maintenance=int(item["dias_sem_manutencao"]),
                operational_risk=float(item["indice_risco_operacional"]),
                contractual_weight=_resolve_contractual_weight(item["zona"]),
                maintenance_history_count=int(item["historico_rocadas"]),
                operational_status=item["status_operacional"],
                observations=item.get("metadata", {}).get("observacoes", []),
                collected_at=datetime.fromisoformat(item["metadata"]["data_coleta"]),
            )
            for item in payload.get("microtrechos", [])
        ]
        await repository.save_many(microsegments)
        await session.commit()


def _resolve_contractual_weight(zone: str) -> int:
    zone_weights = {
        "urbana": 3,
        "rural_estavel": 2,
        "critica": 5,
        "recuperada": 4,
        "monitoramento": 3,
    }
    return zone_weights.get(zone, 3)
