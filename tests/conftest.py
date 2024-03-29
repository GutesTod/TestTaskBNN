from asyncio import Task
from typing import Optional

import pytest
from httpx import AsyncClient
from yarl import URL

import core.database as database
from alembic.command import upgrade
from core.settings import settings

from tests.db_utils import alembic_config_from_url, tmp_database


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio", {"use_uvloop": True}


@pytest.fixture(scope="session")
def pg_url():
    """Provides base PostgreSQL URL for creating temporary databases."""
    return URL(settings.database_url)


@pytest.fixture(scope="session")
async def migrated_postgres_template(pg_url):
    """
    Creates temporary database and applies migrations.

    Has "session" scope, so is called only once per tests run.
    """
    async with tmp_database(pg_url, "pytest") as tmp_url:
        alembic_config = alembic_config_from_url(tmp_url)
        # sometimes we have so called data-migrations.
        # they can call different db-related functions etc..
        # so we modify our settings
        settings.database_url = tmp_url

        # It is important to always close the connections at the end of such migrations,
        # or we will get errors like `source database is being accessed by other users`

        upgrade(alembic_config, "head")
        await MIGRATION_TASK

        yield tmp_url


@pytest.fixture(scope="session")
async def sessionmanager_for_tests(migrated_postgres_template):
    database.db_manager.init(db_url=migrated_postgres_template)
    yield database.db_manager
    await database.db_manager.close()


@pytest.fixture()
async def session(sessionmanager_for_tests):
    async with database.db_manager.session() as session:
        yield session
    async with database.db_manager.connect() as conn:
        for table in reversed(database.OrmBase.metadata.sorted_tables):
            await conn.execute(table.delete())
        await conn.commit()


# Explained in supporting article
MIGRATION_TASK: Optional[Task] = None


@pytest.fixture()
def app():
    from main import app

    yield app


@pytest.fixture()
async def client(session, app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
