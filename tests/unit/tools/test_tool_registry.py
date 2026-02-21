"""Tests for MCP tool registry classification."""

from src.tools.registry import TOOL_REGISTRY, classify_tool


def test_registry_contains_expected_tools():
    assert "health_check" in TOOL_REGISTRY
    assert "create_network" in TOOL_REGISTRY
    assert "get_client_details" in TOOL_REGISTRY


def test_classification_read_only():
    assert classify_tool("health_check") == "read_only"


def test_classification_mutating():
    assert classify_tool("create_network") == "mutating"
    assert classify_tool("execute_port_action") == "mutating"


def test_classification_risky_read():
    assert classify_tool("get_client_details") == "risky_read"
