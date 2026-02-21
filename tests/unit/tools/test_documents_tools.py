"""Unit tests for Deep Research configuration documents tools."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.tools.documents import fetch_document, list_document_ids, search_documents


@pytest.fixture
def mock_settings() -> MagicMock:
    settings = MagicMock()
    settings.log_level = "INFO"
    settings.api_type = MagicMock()
    settings.api_type.value = "cloud-ea"
    settings.base_url = "https://api.ui.com"
    settings.include_macs = False
    settings.include_serials = False
    settings.include_public_ip = False
    settings.get_integration_path = MagicMock(return_value="/integration/v1/sites")
    return settings


def _mock_api_data() -> dict[str, list[dict]]:
    return {
        "/ea/sites": [{"id": "site-1", "name": "HQ"}],
        "/ea/sites/site-1/devices": [
            {
                "_id": "device-1",
                "name": "Gateway",
                "type": "ugw",
                "model": "UXG",
                "state": 1,
                "mac": "aa:bb:cc:dd:ee:ff",
                "serial": "ABCDEF123456",
                "ip": "192.168.1.1",
            }
        ],
        "/ea/sites/site-1/stat/alluser": [
            {
                "mac": "11:22:33:44:55:66",
                "hostname": "workstation-1",
                "name": "Owner Name",
            }
        ],
        "/ea/sites/site-1/rest/networkconf": [
            {
                "_id": "net-1",
                "name": "LAN",
                "purpose": "corporate",
                "vlan_id": 1,
                "ip_subnet": "10.0.1.0/24",
                "dhcpd_enabled": True,
            }
        ],
        "/ea/sites/site-1/rest/wlanconf": [
            {
                "_id": "wlan-1",
                "name": "CorpWiFi",
                "security": "wpapsk",
                "enabled": True,
                "x_passphrase": "super-secret-psk",
                "vlan": 1,
            }
        ],
        "/ea/sites/site-1/rest/firewallrule": [
            {
                "_id": "rule-1",
                "name": "Allow DNS",
                "action": "accept",
                "ruleset": "LAN_IN",
                "enabled": True,
            }
        ],
        "/ea/sites/site-1/rest/portconf": [
            {
                "_id": "profile-1",
                "name": "Default",
                "native_networkconf_id": "net-1",
                "poe_mode": "auto",
            }
        ],
        "/integration/v1/sites/site-1/wans": [
            {
                "name": "WAN1",
                "public_ip": "198.51.100.10",
            }
        ],
    }


def _mock_client_for_data(endpoint_data: dict[str, list[dict]]) -> AsyncMock:
    mock_client = AsyncMock()
    mock_client.authenticate = AsyncMock()

    async def get_side_effect(endpoint: str, params=None):  # noqa: ARG001
        if endpoint in endpoint_data:
            return endpoint_data[endpoint]
        raise RuntimeError(f"Unexpected endpoint: {endpoint}")

    mock_client.get = AsyncMock(side_effect=get_side_effect)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    return mock_client


@pytest.mark.unit
@pytest.mark.asyncio
async def test_search_documents_returns_results_for_keyword(mock_settings: MagicMock) -> None:
    with patch("src.tools.documents.UniFiClient") as mock_client_class:
        mock_client_class.return_value = _mock_client_for_data(_mock_api_data())

        results = await search_documents("wifi", mock_settings)

        assert results
        assert any(result["id"] == "wifi_ssids_security" for result in results)
        assert all("snippet" in result for result in results)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_fetch_document_returns_text_for_all_known_ids(mock_settings: MagicMock) -> None:
    with patch("src.tools.documents.UniFiClient") as mock_client_class:
        mock_client_class.return_value = _mock_client_for_data(_mock_api_data())

        for doc_id in list_document_ids():
            doc = await fetch_document(doc_id, mock_settings)
            assert doc["id"] == doc_id
            assert isinstance(doc["text"], str)
            assert len(doc["text"]) > 0


@pytest.mark.unit
@pytest.mark.asyncio
async def test_fetch_document_redaction_flags_work(mock_settings: MagicMock) -> None:
    with patch("src.tools.documents.UniFiClient") as mock_client_class:
        mock_client_class.return_value = _mock_client_for_data(_mock_api_data())

        redacted = await fetch_document("inventory_snapshot", mock_settings)

    assert "aa:bb:cc:dd:ee:ff" not in redacted["text"]
    assert "ABCDEF123456" not in redacted["text"]
    assert "198.51.100.10" not in redacted["text"]
    assert "super-secret-psk" not in redacted["text"]

    mock_settings.include_macs = True
    mock_settings.include_serials = True
    mock_settings.include_public_ip = True

    with patch("src.tools.documents.UniFiClient") as mock_client_class:
        mock_client_class.return_value = _mock_client_for_data(_mock_api_data())

        unredacted = await fetch_document("inventory_snapshot", mock_settings)

    assert "aa:bb:cc:dd:ee:ff" in unredacted["text"]
    assert "ABCDEF123456" in unredacted["text"]
    assert "198.51.100.10" in unredacted["text"]
    assert "super-secret-psk" not in unredacted["text"]
