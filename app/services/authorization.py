from dataclasses import dataclass

from fastapi import Header, HTTPException


@dataclass(frozen=True)
class Actor:
    actor_id: str
    role: str


ALLOWED_ACTION_ROLES = {"operator", "admin", "ai_agent"}


def authorize_action(actor: Actor) -> None:
    if actor.role not in ALLOWED_ACTION_ROLES:
        raise PermissionError(f"Role '{actor.role}' is not authorized for plant actions")


def get_actor(
    x_actor_id: str | None = Header(default=None),
    x_actor_role: str | None = Header(default=None),
) -> Actor:
    if not x_actor_id or not x_actor_role:
        raise HTTPException(status_code=401, detail="Actor identity and role are required")
    actor = Actor(actor_id=x_actor_id, role=x_actor_role)
    try:
        authorize_action(actor)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    return actor
