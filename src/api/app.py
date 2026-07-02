from contextlib import asynccontextmanager
from typing import Coroutine
from fastapi import FastAPI
from src.db.session import init_db
from src.elastic.search import elasticsearcher
from src.api.crud import crud_router
from src.api.search import search_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await elasticsearcher.create_index()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="APR test task",
    description="API to search among posts using elasticsearch",
    version="1.0.0",
)

app.include_router(crud_router)
app.include_router(search_router)
