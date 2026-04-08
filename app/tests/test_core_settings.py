from __future__ import annotations

from pytest import MonkeyPatch

from app.core.config import Environment, Settings


def test_settings_env_prefix_and_nested_loading(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("BTP_ENV", "production")
    monkeypatch.setenv("BTP_API__PORT", "9100")
    monkeypatch.setenv("BTP_DATABASE__HOST", "db.internal")

    settings = Settings()

    assert settings.env is Environment.PRODUCTION
    assert settings.api.port == 9100
    assert settings.database.host == "db.internal"
    assert settings.is_prod


def test_settings_security_validation(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("BTP_SECURITY__ENABLED", "true")
    monkeypatch.delenv("BTP_SECURITY__JWT_ISSUER", raising=False)
    monkeypatch.delenv("BTP_SECURITY__JWT_AUDIENCE", raising=False)

    try:
        Settings()
    except ValueError as exc:
        assert "issuer/audience" in str(exc)
    else:
        raise AssertionError(
            "Settings() should fail when security is enabled without issuer/audience"
        )
