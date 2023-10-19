import os
from typing import List

from dotenv import load_dotenv
from pydantic import AnyHttpUrl

load_dotenv()


def get_db_url(driver="asyncpg"):
    return "postgresql+{PG_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        PG_DRIVER=driver,
        DB_USER=os.environ.get("POSTGRES_USER"),
        DB_PASSWORD=os.environ.get("POSTGRES_PASSWORD"),
        DB_HOST=os.environ.get("DB_HOST"),
        DB_PORT=os.environ.get("DB_PORT"),
        DB_NAME=os.environ.get("POSTGRES_DB"),
    )


def get_test_db_url():
    return "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}".format(
        DB_USER=os.environ.get("POSTGRES_USER_TEST"),
        DB_PASSWORD=os.environ.get("POSTGRES_PASSWORD_TEST"),
        DB_HOST=os.environ.get("DB_HOST_TEST"),
        DB_PORT=os.environ.get("DB_PORT_TEST"),
        DB_NAME=os.environ.get("POSTGRES_DB_TEST"),
    )


BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
DATABASE_URL = get_db_url()
TEST_DATABASE_URL = get_test_db_url()
SYNC_DATABASE_URL = get_db_url("psycopg2")


ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
JWT_REFRESH_SECRET_KEY = "JWT_REFRESH_SECRET_KEY"
SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
