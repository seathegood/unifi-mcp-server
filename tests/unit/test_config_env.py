import pytest

from src.config.config import APIType, Settings


@pytest.mark.unit
def test_settings_with_new_env_names(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("UNIFI_API_KEY", "key-new")
    monkeypatch.setenv("UNIFI_API_TYPE", "cloud-ea")
    monkeypatch.setenv("UNIFI_CLOUD_API_URL", "https://api.ui.com")
    monkeypatch.setenv("UNIFI_RATE_LIMIT_REQUESTS", "150")
    monkeypatch.setenv("UNIFI_RATE_LIMIT_PERIOD", "30")
    monkeypatch.setenv("UNIFI_REQUEST_TIMEOUT", "15")
    monkeypatch.setenv("UNIFI_MAX_RETRIES", "4")
    monkeypatch.setenv("MCP_TRANSPORT", "http")
    monkeypatch.setenv("MCP_HOST", "127.0.0.1")
    monkeypatch.setenv("MCP_PORT", "9090")
    monkeypatch.setenv("MCP_PATH", "/mcp")
    monkeypatch.setenv("LOG_LEVEL", "debug")

    settings = Settings()

    assert settings.api_key == "key-new"
    assert settings.api_type is APIType.CLOUD_EA
    assert settings.base_url == "https://api.ui.com"
    assert settings.rate_limit_requests == 150
    assert settings.rate_limit_period == 30
    assert settings.request_timeout == 15
    assert settings.max_retries == 4
    assert settings.mcp_transport == "http"
    assert settings.mcp_host == "127.0.0.1"
    assert settings.mcp_port == 9090
    assert settings.mcp_path == "/mcp"
    assert settings.log_level == "DEBUG"


@pytest.mark.unit
def test_settings_with_legacy_env_names(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("UNIFI_API_KEY", "key-legacy")
    monkeypatch.setenv("UNIFI_API_TYPE", "local")
    monkeypatch.setenv("UNIFI_HOST", "192.0.2.10")
    monkeypatch.setenv("UNIFI_PORT", "8443")
    monkeypatch.setenv("UNIFI_VERIFY_SSL", "false")
    monkeypatch.setenv("UNIFI_SITE", "mysite")
    monkeypatch.setenv("UNIFI_RATE_LIMIT", "50")
    monkeypatch.setenv("UNIFI_TIMEOUT", "12")

    settings = Settings()

    assert settings.api_key == "key-legacy"
    assert settings.api_type is APIType.LOCAL
    assert settings.local_host == "192.0.2.10"
    assert settings.local_port == 8443
    assert settings.verify_ssl is False
    assert settings.default_site == "mysite"
    assert settings.rate_limit_requests == 50
    assert settings.request_timeout == 12
    assert settings.base_url == "https://192.0.2.10:8443"
