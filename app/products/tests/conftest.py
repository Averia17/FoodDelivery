import asyncio
from contextlib import asynccontextmanager

import pytest
import pytest_asyncio

from config import settings
from config.db.manager import get_db, sessionmanager
from main import app


@asynccontextmanager
@pytest_asyncio.fixture(autouse=True, scope="session")
async def create_session():
    sessionmanager.init(settings.TEST_DATABASE_URL)
    print("session starts")
    async with sessionmanager.connect() as connection:
        await sessionmanager.create_all(connection)
    yield
    print("session finishes")
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
    await sessionmanager.close()


async def override_get_db():
    async with sessionmanager.session() as session:
        print("getting test db")
        yield session


@pytest_asyncio.fixture(autouse=True)
async def change_db_in_app():
    app.dependency_overrides[get_db] = override_get_db
    print("changing_db_in_app")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
