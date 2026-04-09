from __future__ import annotations

from enum import StrEnum

from pydantic import Field, SecretStr, model_validator
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    TEST = "test"
    PRODUCTION = "production"


class ApiSettings(BaseSettings):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    workers: int = Field(default=1, ge=1)


class DatabaseSettings(BaseSettings):
    host: str = Field(default="postgres")
    port: int = Field(default=5432, ge=1, le=65535)
    name: str = Field(default="trading", min_length=1)
    user: str = Field(default="trading", min_length=1)
    password: SecretStr = Field(default=SecretStr("trading"))
    echo: bool = Field(default=False)
    pool_size: int = Field(default=10, ge=1)
    max_overflow: int = Field(default=20, ge=0)

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn(
            f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"
        )


class RedisSettings(BaseSettings):
    url: str = Field(default="redis://redis:6379/0", min_length=1)
    socket_timeout_seconds: float = Field(default=5.0, gt=0)


class ObservabilitySettings(BaseSettings):
    service_name: str = Field(default="bot-trading-platform", min_length=1)
    log_level: str = Field(default="INFO", min_length=1)
    metrics_enabled: bool = Field(default=True)


class SecuritySettings(BaseSettings):
    enabled: bool = Field(default=False)
    jwt_issuer: str = Field(default="")
    jwt_audience: str = Field(default="")


class SimulationSettings(BaseSettings):
    enabled: bool = Field(default=False)
    fill_latency_ms: int = Field(default=100, ge=0)


class AdapterSettings(BaseSettings):
    request_timeout_seconds: float = Field(default=5.0, gt=0)
    max_retries: int = Field(default=2, ge=0)


class RiskDefaultsSettings(BaseSettings):
    max_order_notional: float = Field(default=10_000.0, gt=0)
    max_daily_loss: float = Field(default=1_000.0, gt=0)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BTP_",
        env_nested_delimiter="__",
        extra="ignore",
        case_sensitive=False,
    )

    env: Environment = Field(default=Environment.DEVELOPMENT)
    api: ApiSettings = Field(default_factory=ApiSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    simulation: SimulationSettings = Field(default_factory=SimulationSettings)
    adapters: AdapterSettings = Field(default_factory=AdapterSettings)
    risk_defaults: RiskDefaultsSettings = Field(default_factory=RiskDefaultsSettings)

    @model_validator(mode="after")
    def validate_security_config(self) -> Settings:
        if self.security.enabled and (
            not self.security.jwt_issuer or not self.security.jwt_audience
        ):
            raise ValueError("security issuer/audience must be set when security is enabled")
        return self

    @property
    def is_dev(self) -> bool:
        return self.env is Environment.DEVELOPMENT

    @property
    def is_test(self) -> bool:
        return self.env is Environment.TEST

    @property
    def is_prod(self) -> bool:
        return self.env is Environment.PRODUCTION


_cached_settings: Settings | None = None


def get_settings() -> Settings:
    global _cached_settings
    if _cached_settings is None:
        _cached_settings = Settings()
    return _cached_settings


def reset_settings_cache() -> None:
    global _cached_settings
    _cached_settings = None
