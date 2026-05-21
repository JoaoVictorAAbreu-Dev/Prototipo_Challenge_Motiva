"""
SQLAlchemy Models - Database persistence models
"""

from datetime import datetime
from sqlalchemy import Column, String, Float, Enum, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

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
