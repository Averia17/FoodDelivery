import asyncio
import inspect

import factory
import pytest
import pytest_asyncio
from httpx import AsyncClient
from pytest_factoryboy import register

from config.db import Base
from config.db.manager import get_db, sessionmanager
from config.settings import DATABASE_URL
from main import app
from products.categories.models import Category
from products.ingredients.models import Ingredient
from products.models import Product
from users.auth.services import get_password_hash
from users.models import User


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://localhost") as async_client:
        yield async_client


@pytest_asyncio.fixture
async def manager_token(client, user_factory):
    password = "some_password"
    hash_password = get_password_hash(password)
    user = await user_factory(password=hash_password, is_manager=True)
    data = {"username": user.email, "password": password}

    resp = await client.post(url="/api/auth/token", data=data)
    access_token = resp.json()["access_token"]
    return access_token


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def connection_test(event_loop):
    sessionmanager.init(DATABASE_URL)
    yield
    await sessionmanager.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest_asyncio.fixture
async def test_db():
    async with sessionmanager.session() as session:
        yield session


class AsyncSQLAlchemyFactory(factory.alchemy.SQLAlchemyModelFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():
            async with sessionmanager.session() as db:
                for key, value in kwargs.items():
                    if inspect.isawaitable(value):
                        obj = await value
                        # SubFactory return object but we want id of the object
                        if isinstance(obj, Base) and hasattr(obj, "id"):
                            kwargs[key] = obj.id
                return await model_class.create(db, *args, **kwargs)

        return asyncio.create_task(maker_coroutine())

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]


@register
class CategoryFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda index: f"Ingredient {index}")


@register
class ProductFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda index: f"Ingredient {index}")
    category_id = factory.SubFactory(CategoryFactory)
    price = factory.Faker("random_digit")


@register
class UserFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    password = factory.Faker("pystr")
    phone_number = factory.Sequence(lambda index: f"+37529112223{index}")


@register
class IngredientFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = Ingredient

    name = factory.Sequence(lambda index: f"Ingredient {index}")
