import pytest


@pytest.mark.django_db
def test_board_get(client, user_token):

    data = {
        "title": "Test",
    }

    response = client.post("/goals/board/create", data=data)


    board = response.data

    response = client.get("/goals/board/" + str(board['id']))
    response.data.pop("participants")

    assert response.status_code == 200
    assert response.data == board



@pytest.mark.django_db
def test_board_bad_get(client, user_token):

    response = client.get("/goals/board/123" )

    assert response.status_code == 404
