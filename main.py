import contextlib
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

import core.database as database
from core.web import core_router
from core.settings import settings


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    database.db_manager.init(settings.database_url)
    yield
    
    await database.db_manager.close()


app = FastAPI(title="API for BashNIPINeft", lifespan=lifespan)
app.include_router(core_router, tags=["api"])

if __name__ == "__main__":
    # There are a lot of parameters for uvicorn, you should check the docs
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
    )