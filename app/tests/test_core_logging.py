from app.core.config import Settings
from app.core.logging import (
    bind_correlation_id,
    clear_correlation_id,
    configure_logging,
    get_correlation_id,
)


def test_correlation_id_binding_and_clearing() -> None:
    clear_correlation_id()
    generated = get_correlation_id()
    assert generated.startswith("corr_")

    explicit = bind_correlation_id("corr_custom")
    assert explicit == "corr_custom"
    assert get_correlation_id() == "corr_custom"

    clear_correlation_id()
    regenerated = get_correlation_id()
    assert regenerated.startswith("corr_")
    assert regenerated != "corr_custom"


def test_configure_logging_runs_for_dev() -> None:
    settings = Settings()
    configure_logging(settings)
