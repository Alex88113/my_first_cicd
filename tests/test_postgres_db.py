import pytest
from pydantic import ValidationError

from src.my_first_cicd.configs.postgres_config import DataBaseConfig


# 1. Все поля загружаются из переменных окружения
def test_load_all_fields(monkeypatch):
    monkeypatch.setenv("PSQL_USER", "postgres")
    monkeypatch.setenv("PSQL_PASSWORD", "secret")
    monkeypatch.setenv("PSQL_PORT", "5432")
    monkeypatch.setenv("PSQL_HOST", "localhost")
    monkeypatch.setenv("DATABASE_PATH", "postgresql+asyncpg://localhost/db")

    cfg = DataBaseConfig()

    assert cfg.PSQL_USER == "postgres"
    assert cfg.PSQL_PASSWORD == "secret"
    assert cfg.PSQL_PORT == "5432"
    assert cfg.PSQL_HOST == "localhost"
    assert cfg.DATABASE_PATH == "postgresql+asyncpg://localhost/db"


# 2. Все поля обязательны — без env ValidationError
def test_missing_fields_raises(monkeypatch):
    for key in ("PSQL_USER", "PSQL_PASSWORD", "PSQL_PORT", "PSQL_HOST", "DATABASE_PATH"):
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(ValidationError):
        DataBaseConfig()


# 3. Лишние переменные игнорируются (extra='ignore')
def test_extra_env_ignored(monkeypatch):
    monkeypatch.setenv("PSQL_USER", "postgres")
    monkeypatch.setenv("PSQL_PASSWORD", "secret")
    monkeypatch.setenv("PSQL_PORT", "5432")
    monkeypatch.setenv("PSQL_HOST", "localhost")
    monkeypatch.setenv("DATABASE_PATH", "postgresql+asyncpg://localhost/db")
    monkeypatch.setenv("SOME_EXTRA_VAR", "should_be_ignored")

    cfg = DataBaseConfig()

    assert not hasattr(cfg, "SOME_EXTRA_VAR")


# 4. case_sensitive=True — имя в нижнем регистре не подхватывается
def test_case_sensitive(monkeypatch):
    monkeypatch.setenv("psql_user", "lowercase")
    monkeypatch.setenv("PSQL_PASSWORD", "secret")
    monkeypatch.setenv("PSQL_PORT", "5432")
    monkeypatch.setenv("PSQL_HOST", "localhost")
    monkeypatch.setenv("DATABASE_PATH", "postgresql+asyncpg://localhost/db")
    monkeypatch.delenv("PSQL_USER", raising=False)

    with pytest.raises(ValidationError):
        DataBaseConfig()