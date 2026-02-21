"""Plan/apply registry for mutating operations."""

from __future__ import annotations

import hashlib
import os
import secrets
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from ..utils import ValidationError

PLAN_TTL_SECONDS = 600


@dataclass
class PlannedChange:
    """A planned change awaiting explicit caller confirmation and apply."""

    plan_id: str
    created_at: datetime
    expires_at: datetime
    action_type: str
    payload: dict[str, Any]
    diff: dict[str, Any]
    warnings: list[str]
    confirmation_token_hash: str
    executor: Callable[[], Awaitable[Any]] | None = None
    applied: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


_PLANNED_CHANGES: dict[str, PlannedChange] = {}


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _now_utc() -> datetime:
    return datetime.now(UTC)


def _cleanup_expired_plans() -> None:
    now = _now_utc()
    expired_ids = [plan_id for plan_id, plan in _PLANNED_CHANGES.items() if now > plan.expires_at]
    for plan_id in expired_ids:
        _PLANNED_CHANGES.pop(plan_id, None)


def _token_matches(plan: PlannedChange, confirmation_token: str) -> bool:
    if not confirmation_token:
        return False

    token_hash = _hash_token(confirmation_token)
    if token_hash == plan.confirmation_token_hash:
        return True

    env_token = os.getenv("MCP_CONFIRM_TOKEN", "")
    if not env_token:
        return False
    return secrets.compare_digest(confirmation_token, env_token)


def create_plan(
    *,
    action_type: str,
    payload: dict[str, Any],
    diff: dict[str, Any],
    warnings: list[str] | None = None,
    executor: Callable[[], Awaitable[Any]] | None = None,
    ttl_seconds: int = PLAN_TTL_SECONDS,
) -> dict[str, Any]:
    """Create a short-lived plan for a mutating action."""
    if not action_type:
        raise ValidationError("action_type is required")
    if not isinstance(payload, dict):
        raise ValidationError("payload must be an object")
    if not isinstance(diff, dict):
        raise ValidationError("diff must be an object")
    if ttl_seconds <= 0:
        raise ValidationError("ttl_seconds must be > 0")

    _cleanup_expired_plans()

    created_at = _now_utc()
    expires_at = created_at + timedelta(seconds=ttl_seconds)
    plan_id = f"plan_{uuid4().hex}"
    confirmation_token = secrets.token_urlsafe(24)

    plan = PlannedChange(
        plan_id=plan_id,
        created_at=created_at,
        expires_at=expires_at,
        action_type=action_type,
        payload=payload,
        diff=diff,
        warnings=warnings or [],
        confirmation_token_hash=_hash_token(confirmation_token),
        executor=executor,
    )
    _PLANNED_CHANGES[plan_id] = plan

    return {
        "plan_id": plan.plan_id,
        "created_at": plan.created_at.isoformat(),
        "expires_at": plan.expires_at.isoformat(),
        "action_type": plan.action_type,
        "payload": plan.payload,
        "diff": plan.diff,
        "warnings": plan.warnings,
        "confirmation_token": confirmation_token,
    }


def _get_valid_plan(plan_id: str, confirmation_token: str) -> PlannedChange:
    if not confirmation_token:
        raise ValidationError("confirmation_token is required")

    _cleanup_expired_plans()

    plan = _PLANNED_CHANGES.get(plan_id)
    if plan is None:
        raise ValidationError(f"unknown plan_id '{plan_id}'")
    if plan.applied:
        raise ValidationError(f"plan '{plan_id}' has already been applied")
    if _now_utc() > plan.expires_at:
        raise ValidationError(f"plan '{plan_id}' has expired")
    if not _token_matches(plan, confirmation_token):
        raise ValidationError("invalid confirmation_token")

    return plan


async def apply_plan(plan_id: str, confirmation_token: str) -> dict[str, Any]:
    """Apply a previously-created plan after token confirmation."""
    plan = _get_valid_plan(plan_id, confirmation_token)
    plan.applied = True

    if plan.executor is None:
        return {
            "status": "accepted",
            "plan_id": plan.plan_id,
            "action_type": plan.action_type,
            "applied": False,
            "message": "No executor attached to this plan; no mutation performed.",
            "diff": plan.diff,
            "warnings": plan.warnings,
        }

    result = await plan.executor()
    return {
        "status": "applied",
        "plan_id": plan.plan_id,
        "action_type": plan.action_type,
        "applied": True,
        "result": result,
        "warnings": plan.warnings,
    }


def clear_plan_registry() -> None:
    """Clear all in-memory plans (primarily for tests)."""
    _PLANNED_CHANGES.clear()


def plan_change(change_request: dict[str, Any]) -> dict[str, Any]:
    """Backward-compatible generic change plan scaffold.

    Args:
        change_request: Requested operation metadata and desired parameters
    """
    if not isinstance(change_request, dict) or not change_request:
        raise ValidationError("change_request must be a non-empty object")

    diff = {
        "requested_change": change_request,
        "before": "No preflight snapshot captured (scaffolding only)",
        "after": "No mutation executed (plan only)",
    }
    warnings = [
        "Generic scaffold mode: no UniFi write operation bound to this plan.",
        "Store confirmation_token securely; apply_change requires an exact token match.",
    ]

    return create_plan(
        action_type=change_request.get("tool", "generic_change"),
        payload=change_request,
        diff=diff,
        warnings=warnings,
        executor=None,
    )


def apply_change(plan_id: str, confirmation_token: str) -> dict[str, Any]:
    """Backward-compatible synchronous apply for scaffold plans."""
    plan = _get_valid_plan(plan_id, confirmation_token)
    plan.applied = True

    return {
        "status": "accepted",
        "plan_id": plan.plan_id,
        "action_type": plan.action_type,
        "applied": False,
        "message": "Synchronous scaffold apply: no executor is run by apply_change().",
        "diff": plan.diff,
        "warnings": plan.warnings,
    }
