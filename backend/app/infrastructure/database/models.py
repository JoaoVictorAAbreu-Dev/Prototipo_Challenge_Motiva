"""
SQLAlchemy Models - Database persistence models
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import declarative_base

try:
    from geoalchemy2 import Geometry
except ModuleNotFoundError:  # pragma: no cover - local fallback only
    def Geometry(*_args, **_kwargs):
        return String

Base = declarative_base()


class MonitorModel(Base):
    """SQLAlchemy model for Monitor entity"""

    __tablename__ = "monitors"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(1000))
    monitor_type = Column(String(50), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="active", index=True)
    center_point = Column(
        Geometry("POINT", srid=4326), nullable=False, index=True
    )
    radius_meters = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<MonitorModel(id={self.id}, name={self.name})>"


class MicroSegmentModel(Base):
    """SQLAlchemy model for the operational mesh."""

    __tablename__ = "microsegments"

    id = Column(String(50), primary_key=True)
    monitor_id = Column(String(36), nullable=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    road_name = Column(String(255), nullable=False)
    km_start = Column(Float, nullable=False, index=True)
    km_end = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    zone = Column(String(50), nullable=False, index=True)
    evi = Column(Float, nullable=False)
    rain_forecast = Column(Float, nullable=False)
    days_without_maintenance = Column(Integer, nullable=False)
    operational_risk = Column(Float, nullable=False)
    contractual_weight = Column(Integer, nullable=False)
    maintenance_history_count = Column(Integer, nullable=False)
    operational_status = Column(String(50), nullable=False, index=True)
    observations = Column(Text, nullable=False, default="[]")
    collected_at = Column(DateTime, nullable=False)
    location_point = Column(Geometry("POINT", srid=4326), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<MicroSegmentModel(id={self.id}, name={self.name})>"
