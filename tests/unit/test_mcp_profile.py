"""Tests for MCP tool registration profiles in src.main."""

import importlib
import sys
import types

import pytest


class FakeFastMCP:
    """Minimal FastMCP stub for testing registration behavior."""

    def __init__(self, name: str):
        self.name = name
        self._tools: dict[str, object] = {}

    def tool(self):
        def _decorator(func):
            self._tools[func.__name__] = func
            return func

        return _decorator

    def resource(self, *_args, **_kwargs):
        def _decorator(func):
            return func

        return _decorator

    async def run_http_async(self, *_args, **_kwargs):
        return None

    def run(self, *_args, **_kwargs):
        return None


def _install_stub_modules(monkeypatch: pytest.MonkeyPatch) -> None:
    fastmcp = types.ModuleType("fastmcp")
    fastmcp.FastMCP = FakeFastMCP
    monkeypatch.setitem(sys.modules, "fastmcp", fastmcp)

    agnost = types.ModuleType("agnost")
    agnost.config = lambda **kwargs: kwargs
    agnost.track = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, "agnost", agnost)


def _import_main_for_profile(monkeypatch: pytest.MonkeyPatch, profile: str):
    _install_stub_modules(monkeypatch)
    monkeypatch.setenv("UNIFI_API_KEY", "test-key")
    monkeypatch.setenv("UNIFI_API_TYPE", "cloud-ea")
    monkeypatch.setenv("MCP_PROFILE", profile)
    monkeypatch.delenv("DEBUG", raising=False)
    sys.modules.pop("src.main", None)
    return importlib.import_module("src.main")


@pytest.mark.unit
def test_deep_research_profile_registers_only_deep_research_tools(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    main_module = _import_main_for_profile(monkeypatch, "deep-research")
    assert set(main_module.mcp._tools) == {"health_check", "search", "fetch"}


@pytest.mark.unit
def test_full_profile_registers_additional_non_document_tools(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    main_module = _import_main_for_profile(monkeypatch, "full")
    tool_names = set(main_module.mcp._tools)

    assert {"health_check", "search", "fetch"}.issubset(tool_names)
    assert "list_all_sites" in tool_names
