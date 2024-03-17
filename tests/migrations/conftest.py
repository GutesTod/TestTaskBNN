import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from tests.db_utils import alembic_config_from_url, tmp_database


@pytest.fixture()
async def postgres(pg_url):
    """
    Создает пустую временную базу данных.
    """
    async with tmp_database(pg_url, "pytest") as tmp_url:
        yield tmp_url


@pytest.fixture()
async def postgres_engine(postgres):
    """
    Движок SQLAlchemy, привязанный к временной базе данных.
    """
    engine = create_async_engine(
        url=postgres,
        pool_pre_ping=True,
    )
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture()
def alembic_config(postgres):
    """
    Объект конфигурации Alembic, привязанный к временной базе данных.
    """
    return alembic_config_from_url(postgres)
