from uuid import uuid4
from fastapi import APIRouter, Depends, status
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
            "data": {"sum": sum(request.array)}
        }
    )

# Асинхронный метод
@core_router.post("/api/async", status_code=status.HTTP_201_CREATED)
async def sum_async(request: SumRequest, session: AsyncSession = Depends(database.get_session)) ->  JSONResponse:
    session_id = str(uuid4())

    # Сохранить данные в базе данных
    result = database.SumResult(
        session_id = session_id,
        sum=sum(request.array)
    )
    session.add(result)
    await session.commit()

    return JSONResponse(
        content={
            "status": "ok",
            "data" : {"session_id": session_id}
        },
        status_code=status.HTTP_201_CREATED,
    )

# Получение результата
@core_router.get("/api/async/{session_id}")
async def get_result(session_id: str, session: AsyncSession = Depends(database.get_session)) ->  JSONResponse:
    # Получить результат из базы данных
    query = select(database.SumResult).filter(database.SumResult.session_id == session_id)
    result = (await session.execute(query)).scalars().first()

    if result is None:
        return JSONResponse(
            content={"status": "error", "message": "Sum not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data" : {
                "session_id": result.session_id,
                "sum": result.sum
            }
        }
    )
