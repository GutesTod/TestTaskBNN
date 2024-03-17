from sqlalchemy import text

import core.database as database


async def test_orm_session(session):
    user = database.SumResult(
        session_id="3251009e-1364-4152-a540-c7f8ed2d193f",
        sum=25,
    )
    session.add(user)
    await session.commit()

    rows = await session.execute(text('SELECT session_id, sum FROM "sum_results"'))
    result = list(rows)[0]
    assert isinstance(result[0], int)
    assert result[1] == "3251009e-1364-4152-a540-c7f8ed2d193f"
    assert result[2] == 25
