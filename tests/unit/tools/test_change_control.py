"""Tests for change control scaffolding."""

import pytest

from src.tools.change_control import apply_change, plan_change
from src.utils import ValidationError


def test_plan_change_returns_plan_and_token():
    result = plan_change({"tool": "create_network", "params": {"name": "Guest"}})

    assert "plan_id" in result
    assert "confirmation_token" in result
    assert result["diff"]["requested_change"]["tool"] == "create_network"


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
