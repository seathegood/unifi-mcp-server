"""Tests for plan/apply change control registry."""

import asyncio

import pytest

from src.tools.change_control import apply_change, apply_plan, clear_plan_registry, create_plan, plan_change
from src.utils import ValidationError


@pytest.fixture(autouse=True)
def reset_plan_registry() -> None:
    clear_plan_registry()


def test_plan_change_returns_plan_and_token():
    result = plan_change({"tool": "create_network", "params": {"name": "Guest"}})
    assert "plan_id" in result
    assert "confirmation_token" in result
    assert result["diff"]["requested_change"]["tool"] == "create_network"
    assert "expires_at" in result


def test_apply_change_requires_confirmation_token():
    result = plan_change({"tool": "create_network", "params": {"name": "Guest"}})

    with pytest.raises(ValidationError):
        apply_change(result["plan_id"], "")


def test_apply_change_rejects_invalid_token():
    result = plan_change({"tool": "create_network", "params": {"name": "Guest"}})

    with pytest.raises(ValidationError):
        apply_change(result["plan_id"], "invalid-token")


def test_apply_change_accepts_valid_token_once():
    result = plan_change({"tool": "create_network", "params": {"name": "Guest"}})

    apply_result = apply_change(result["plan_id"], result["confirmation_token"])
    assert apply_result["status"] == "accepted"
    assert apply_result["applied"] is False

    with pytest.raises(ValidationError):
        apply_change(result["plan_id"], result["confirmation_token"])


@pytest.mark.asyncio
async def test_create_plan_and_apply_plan_succeeds_with_correct_token():
    async def _executor() -> dict[str, bool]:
        return {"mutated": True}

    result = create_plan(
        action_type="create_firewall_rule",
        payload={"site_id": "default", "name": "BlockBadHost"},
        diff={"before": {}, "after": {"name": "BlockBadHost"}},
        warnings=["test warning"],
        executor=_executor,
    )

    assert "plan_id" in result
    assert "diff" in result
    assert result["action_type"] == "create_firewall_rule"

    apply_result = await apply_plan(result["plan_id"], result["confirmation_token"])
    assert apply_result["status"] == "applied"
    assert apply_result["applied"] is True
    assert apply_result["result"] == {"mutated": True}


@pytest.mark.asyncio
async def test_apply_plan_fails_without_token():
    result = create_plan(
        action_type="delete_backup",
        payload={"site_id": "default", "backup_filename": "nightly.unf"},
        diff={"before": {"backup": "nightly.unf"}, "after": {"backup": None}},
    )

    with pytest.raises(ValidationError, match="confirmation_token is required"):
        await apply_plan(result["plan_id"], "")


@pytest.mark.asyncio
async def test_apply_plan_fails_after_ttl_expiry():
    result = create_plan(
        action_type="restore_backup",
        payload={"site_id": "default", "backup_filename": "restore.unf"},
        diff={"before": {"controller": "current"}, "after": {"controller": "restore.unf"}},
        ttl_seconds=1,
    )

    await asyncio.sleep(1.1)

    with pytest.raises(ValidationError, match="unknown plan_id|expired"):
        await apply_plan(result["plan_id"], result["confirmation_token"])
