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
        "/api/async/",
        json={"session_id": "064d6016-2d87-4ac8-a175-27e0bb3e220e", "array": [1,2,3,4,5,6]},
    )
    assert response.status_code == status.HTTP_201_CREATED
    new_session_id = response.json()["data"]["session_id"]

    response = await client.get(f"/api/async/{new_session_id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "ok",
        "data": {
            "id": new_session_id,
            "name": "Michael",
            "fullname": "Test Person",
        },
    }
