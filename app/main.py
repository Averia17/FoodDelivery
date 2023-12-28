from contextlib import asynccontextmanager

from config import settings
from config.db.manager import sessionmanager
from config.urls import api_router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager.init(settings.DATABASE_URL)
    yield
    await sessionmanager.close()


app = FastAPI(lifespan=lifespan)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api")


@app.get("/")
def healthcheck():
    return {"app": "working"}