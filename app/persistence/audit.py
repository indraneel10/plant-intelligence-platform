from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.persistence.models import AuditEventModel


def record_audit_event(
    db: Session,
    *,
    event_type: str,
    actor_id: str,
    actor_role: str,
    plant_id: str | None,
    status: str,
    action_type: str | None = None,
    zone_id: str | None = None,
    duration_seconds: int | None = None,
    reason: str | None = None,
    details: str | None = None,
) -> AuditEventModel:
    event = AuditEventModel(
        event_type=event_type,
        actor_id=actor_id,
        actor_role=actor_role,
        plant_id=plant_id,
        status=status,
        action_type=action_type,
        zone_id=zone_id,
        duration_seconds=duration_seconds,
        reason=reason,
        details=details,
        created_at=datetime.now(timezone.utc),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
