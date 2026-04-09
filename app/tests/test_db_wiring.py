from app.core.config import Settings
from app.infrastructure.db import build_engine, build_session_factory


def test_engine_uses_asyncpg_scheme() -> None:
    settings = Settings()
    engine = build_engine(settings)
    assert engine.url.drivername == "postgresql+asyncpg"


def test_session_factory_wiring() -> None:
    settings = Settings()
    engine = build_engine(settings)
    session_factory = build_session_factory(engine)

    assert session_factory is not None
