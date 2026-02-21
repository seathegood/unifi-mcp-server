"""Plan/apply scaffolding for future mutating operations."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

from ..utils import ValidationError

PLAN_TTL_MINUTES = 30


@dataclass
class PlannedChange:
    """A planned change awaiting explicit caller confirmation."""

    plan_id: str
    diff: dict[str, Any]
    warnings: list[str]
    confirmation_token_hash: str
    expires_at: datetime
    applied: bool = False


_PLANNED_CHANGES: dict[str, PlannedChange] = {}


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def plan_change(change_request: dict[str, Any]) -> dict[str, Any]:
    """Create a change plan without applying any mutations.

    Args:
        change_request: Requested operation metadata and desired parameters

    Returns:
        A response containing `plan_id`, `diff`, `warnings`, and a
        `confirmation_token` required by `apply_change`.
    """
    if not isinstance(change_request, dict) or not change_request:
        raise ValidationError("change_request must be a non-empty object")

    plan_id = f"plan_{uuid4().hex}"
    confirmation_token = secrets.token_urlsafe(24)

    diff = {
        "requested_change": change_request,
        "before": "No preflight snapshot captured (scaffolding only)",
        "after": "No mutation executed (plan only)",
    }
    warnings = [
        "Scaffolding mode: plan generated, but no UniFi write operation was executed.",
        "Store confirmation_token securely; apply_change requires an exact token match.",
    ]

    _PLANNED_CHANGES[plan_id] = PlannedChange(
        plan_id=plan_id,
        diff=diff,
        warnings=warnings,
        confirmation_token_hash=_hash_token(confirmation_token),
        expires_at=datetime.now(UTC) + timedelta(minutes=PLAN_TTL_MINUTES),
    )

    return {
        "plan_id": plan_id,
        "diff": diff,
        "warnings": warnings,
        "confirmation_token": confirmation_token,
        "expires_at": _PLANNED_CHANGES[plan_id].expires_at.isoformat(),
    }


def apply_change(plan_id: str, confirmation_token: str) -> dict[str, Any]:
    """Apply a previously planned change after explicit token confirmation.

    This is scaffolding for future write tools and intentionally performs no
    UniFi mutations today.
    """
    if not confirmation_token:
        raise ValidationError("confirmation_token is required")

    plan = _PLANNED_CHANGES.get(plan_id)
    if plan is None:
        raise ValidationError(f"unknown plan_id '{plan_id}'")
    if plan.applied:
        raise ValidationError(f"plan '{plan_id}' has already been applied")
    if datetime.now(UTC) > plan.expires_at:
        raise ValidationError(f"plan '{plan_id}' has expired")
    if _hash_token(confirmation_token) != plan.confirmation_token_hash:
        raise ValidationError("invalid confirmation_token")

    plan.applied = True

    return {
        "status": "accepted",
        "plan_id": plan.plan_id,
        "applied": False,
        "message": "Scaffolding only: no write operation is implemented yet.",
        "diff": plan.diff,
        "warnings": plan.warnings,
    }
