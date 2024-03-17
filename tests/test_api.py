from fastapi import status


async def test_my_api(client, app):
    # Test to show that api is working
    # array: list[int]
    response = await client.post(
        "/api/sync",
        json={"array": [1,2,3,4,5,6]}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok", "data": {"sum": 21}}

    response = await client.post(
        "/api/async",
        json={"array": [1,2,3,4,5,6]},
    )
    assert response.status_code == status.HTTP_201_CREATED
    new_session_id = response.json()["data"]["session_id"]
    assert isinstance(new_session_id, str)
    response = await client.get(f"/api/async/{new_session_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "ok",
        "data": {
            "session_id": new_session_id,
            "sum": 21,
        },
    }
