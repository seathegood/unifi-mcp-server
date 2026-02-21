"""Tests for centralized client/device output redaction."""

from src.utils.redaction import redact_client_device_data


def test_redact_client_device_fields():
    payload = {
        "mac": "00:11:22:33:44:55",
        "ip": "192.168.1.45",
        "hostname": "john-laptop",
        "name": "Living Room AP",
        "stats": {"client_mac": "aa:bb:cc:dd:ee:ff"},
    }

    redacted = redact_client_device_data(payload)

    assert redacted["mac"] == "**:**:**:**:**:55"
    assert redacted["ip"] == "***.***.***.45"
    assert redacted["hostname"].startswith("***")
    assert redacted["name"] == "Living Room AP"
    assert redacted["stats"]["client_mac"] == "**:**:**:**:**:ff"


def test_redact_list_payloads():
    payload = [{"device_mac": "11:22:33:44:55:66"}, {"serial": "ABC123456"}]

    redacted = redact_client_device_data(payload)

    assert redacted[0]["device_mac"] == "**:**:**:**:**:66"
    assert redacted[1]["serial"].startswith("***")
