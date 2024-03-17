from uuid import uuid4
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import core.database as database
from .models import SumRequest

core_router = APIRouter()

@core_router.post("/api/sync")
async def sum_sync(request: SumRequest) -> JSONResponse:
    return JSONResponse(
        content={
            "status": "ok",
            "data": {"sum": sum(SumRequest.array)}
        }
    )

# Асинхронный метод
@core_router.post("/api/async")
async def sum_async(request: SumRequest, session: AsyncSession = Depends(database.get_session)) ->  JSONResponse:
    session_id = str(uuid4())

    # Сохранить данные в базе данных
    result = database.SumResult(
        session_id = session_id,
        sum=sum(request.array)
    )
    session.add(result)
    session.commit()

    return JSONResponse(
        content={
            "status": "ok",
            "data" : {"session_id": session_id}
        }
    )

# Получение результата
@core_router.get("/api/async/{session_id}")
async def get_result(session_id: str, session: AsyncSession = Depends(database.get_session)) ->  JSONResponse:
    # Получить результат из базы данных
    query = select(database.SumResult).filter(database.SumResult.session_id == session_id)
    result = (await session.execute(query)).scalars().first()

    if result is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return JSONResponse(
        content={
            "status": "ok",
            "data" : {
                "session_id": result.session_id,
                "sum": result.sum
            }
        }
    )
