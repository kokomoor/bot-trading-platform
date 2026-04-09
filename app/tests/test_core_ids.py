from app.core.ids import new_correlation_id, new_idempotency_key, new_uuid, new_uuid_str


def test_uuid_generation() -> None:
    assert str(new_uuid())
    assert isinstance(new_uuid_str(), str)


def test_correlation_and_idempotency_prefixes() -> None:
    assert new_correlation_id().startswith("corr_")
    assert new_idempotency_key().startswith("idem_")
    assert new_idempotency_key("risk").startswith("risk_")
