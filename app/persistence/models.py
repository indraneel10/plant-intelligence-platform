from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.persistence.database import Base

class PlantModel(Base):
    __tablename__ = "plants"
    plant_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    species: Mapped[str | None] = mapped_column(String(200), nullable=True)
    zone_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    location_label: Mapped[str | None] = mapped_column(String(200), nullable=True)

class SensorObservationModel(Base):
    __tablename__ = "sensor_observations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_id: Mapped[str] = mapped_column(String(64), index=True)
    plant_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    zone_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    sensor_type: Mapped[str] = mapped_column(String(64), index=True)
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(32))
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

class PlantObservationModel(Base):
    __tablename__ = "plant_observations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plant_id: Mapped[str] = mapped_column(String(64), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    health_score: Mapped[float] = mapped_column(Float)
    wilting_probability: Mapped[float] = mapped_column(Float)
    yellowing_probability: Mapped[float] = mapped_column(Float)
    disease_probability: Mapped[float] = mapped_column(Float)
    image_quality: Mapped[float] = mapped_column(Float)
    leaf_area_ratio: Mapped[float | None] = mapped_column(Float, nullable=True)
    water_stress_probability: Mapped[float | None] = mapped_column(Float, nullable=True)
    heat_stress_probability: Mapped[float | None] = mapped_column(Float, nullable=True)

class VisionObservationModel(Base):
    __tablename__ = "vision_observations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[str] = mapped_column(String(128), index=True)
    plant_id: Mapped[str] = mapped_column(String(64), index=True)
    image_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    model_name: Mapped[str] = mapped_column(String(128))
    model_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    health_score: Mapped[float] = mapped_column(Float)
    wilting_probability: Mapped[float] = mapped_column(Float)
    yellowing_probability: Mapped[float] = mapped_column(Float)
    disease_probability: Mapped[float] = mapped_column(Float)
    image_quality: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)

class DecisionModel(Base):
    __tablename__ = "decisions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plant_id: Mapped[str] = mapped_column(String(64), index=True)
    action: Mapped[str] = mapped_column(String(64))
    reason: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float)
    duration_seconds: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

class IrrigationActionModel(Base):
    __tablename__ = "irrigation_actions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plant_id: Mapped[str] = mapped_column(String(64), index=True)
    zone_id: Mapped[str] = mapped_column(String(64))
    action_type: Mapped[str] = mapped_column(String(64))
    duration_seconds: Mapped[int] = mapped_column(Integer)
    executed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

class AuditEventModel(Base):
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str] = mapped_column(String(64), index=True)
    actor_id: Mapped[str] = mapped_column(String(128), index=True)
    actor_role: Mapped[str] = mapped_column(String(64), index=True)
    plant_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    action_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    zone_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
