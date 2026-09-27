import json
from sqlalchemy.orm import Session

from app.ai.state_tools import get_current_decision, get_current_sensor_state, get_latest_vision_analysis, get_plant_state, get_recent_events, run_monitoring_cycle
from app.persistence.models import (
    DecisionModel,
    IrrigationActionModel,
    PlantModel,
    PlantObservationModel,
    SensorObservationModel,
)


def _serialize(value):
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def get_plant(db: Session, plant_id: str) -> dict:
    plant = db.get(PlantModel, plant_id)
    if plant is None:
        return {"error": "Plant not found", "plant_id": plant_id}
    return {
        "plant_id": plant.plant_id,
        "name": plant.name,
        "species": plant.species,
        "zone_id": plant.zone_id,
        "location_label": plant.location_label,
    }


def get_sensor_history(db: Session, plant_id: str, limit: int = 10) -> list[dict]:
    rows = (
        db.query(SensorObservationModel)
        .filter(SensorObservationModel.plant_id == plant_id)
        .order_by(SensorObservationModel.timestamp.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "sensor_id": r.sensor_id,
            "sensor_type": r.sensor_type,
            "value": r.value,
            "unit": r.unit,
            "zone_id": r.zone_id,
            "timestamp": _serialize(r.timestamp),
        }
        for r in rows
    ]


def get_plant_observations(db: Session, plant_id: str, limit: int = 5) -> list[dict]:
    rows = (
        db.query(PlantObservationModel)
        .filter(PlantObservationModel.plant_id == plant_id)
        .order_by(PlantObservationModel.timestamp.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "timestamp": _serialize(r.timestamp),
            "health_score": r.health_score,
            "wilting_probability": r.wilting_probability,
            "yellowing_probability": r.yellowing_probability,
            "disease_probability": r.disease_probability,
            "image_quality": r.image_quality,
            "leaf_area_ratio": r.leaf_area_ratio,
            "water_stress_probability": r.water_stress_probability,
            "heat_stress_probability": r.heat_stress_probability,
        }
        for r in rows
    ]


def get_decisions(db: Session, plant_id: str, limit: int = 5) -> list[dict]:
    rows = (
        db.query(DecisionModel)
        .filter(DecisionModel.plant_id == plant_id)
        .order_by(DecisionModel.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "action": r.action,
            "reason": r.reason,
            "confidence": r.confidence,
            "duration_seconds": r.duration_seconds,
            "created_at": _serialize(r.created_at),
        }
        for r in rows
    ]


def get_irrigation_history(db: Session, plant_id: str, limit: int = 10) -> list[dict]:
    rows = (
        db.query(IrrigationActionModel)
        .filter(IrrigationActionModel.plant_id == plant_id)
        .order_by(IrrigationActionModel.executed_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "zone_id": r.zone_id,
            "action_type": r.action_type,
            "duration_seconds": r.duration_seconds,
            "executed_at": _serialize(r.executed_at),
        }
        for r in rows
    ]


TOOL_SCHEMAS = [
    {
        "type": "function",
        "name": "get_plant",
        "description": "Get identity and configuration for a plant.",
        "parameters": {
            "type": "object",
            "properties": {"plant_id": {"type": "string"}},
            "required": ["plant_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_sensor_history",
        "description": "Read recent sensor observations for a plant. Use this before making claims about current soil or environmental conditions.",
        "parameters": {
            "type": "object",
            "properties": {
                "plant_id": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 20},
            },
            "required": ["plant_id", "limit"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_plant_observations",
        "description": "Read recent camera/vision-derived plant observations.",
        "parameters": {
            "type": "object",
            "properties": {
                "plant_id": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 10},
            },
            "required": ["plant_id", "limit"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_decisions",
        "description": "Read recent platform decisions and their reasons.",
        "parameters": {
            "type": "object",
            "properties": {
                "plant_id": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 10},
            },
            "required": ["plant_id", "limit"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_plant_state",
        "description": "Get the consolidated current state of a plant.",
        "parameters": {"type": "object", "properties": {"plant_id": {"type": "string"}}, "required": ["plant_id"], "additionalProperties": False},
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_current_sensor_state",
        "description": "Get the latest known sensor values for a plant.",
        "parameters": {"type": "object", "properties": {"plant_id": {"type": "string"}}, "required": ["plant_id"], "additionalProperties": False},
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_latest_vision_analysis",
        "description": "Get the latest vision-derived plant analysis.",
        "parameters": {"type": "object", "properties": {"plant_id": {"type": "string"}}, "required": ["plant_id"], "additionalProperties": False},
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_current_decision",
        "description": "Get the latest platform decision for a plant.",
        "parameters": {"type": "object", "properties": {"plant_id": {"type": "string"}}, "required": ["plant_id"], "additionalProperties": False},
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_recent_events",
        "description": "Get recent observable plant-platform events.",
        "parameters": {"type": "object", "properties": {"plant_id": {"type": "string"}}, "required": ["plant_id"], "additionalProperties": False},
        "strict": True,
    },
    {
        "type": "function",
        "name": "run_monitoring_cycle",
        "description": "Prepare a monitoring-cycle request. This does not directly actuate hardware.",
        "parameters": {"type": "object", "properties": {"plant_id": {"type": "string"}}, "required": ["plant_id"], "additionalProperties": False},
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_irrigation_history",
        "description": "Read recent irrigation actions for a plant.",
        "parameters": {
            "type": "object",
            "properties": {
                "plant_id": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 20},
            },
            "required": ["plant_id", "limit"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def execute_tool(db: Session, name: str, arguments: dict) -> str:
    handlers = {
        "get_plant": get_plant,
        "get_sensor_history": get_sensor_history,
        "get_plant_observations": get_plant_observations,
        "get_decisions": get_decisions,
        "get_irrigation_history": get_irrigation_history,
        "get_plant_state": get_plant_state,
        "get_current_sensor_state": get_current_sensor_state,
        "get_latest_vision_analysis": get_latest_vision_analysis,
        "get_current_decision": get_current_decision,
        "get_recent_events": get_recent_events,
        "run_monitoring_cycle": run_monitoring_cycle,
    }
    handler = handlers.get(name)
    if handler is None:
        return json.dumps({"error": f"Unknown tool: {name}"})
    return json.dumps(handler(db, **arguments), default=_serialize)
