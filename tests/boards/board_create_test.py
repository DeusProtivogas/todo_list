import pytest


@pytest.mark.django_db
def test_board_create(client, user_token):

    data = {
        "title": "Test",
    }

    response = client.post("/goals/board/create", data=data)


    assert response.status_code == 201


@pytest.mark.django_db
def test_board_bad_create(client, user_token):

    data = {
        "title": "",
    }

    response = client.post("/goals/board/create", data=data)


    assert response.status_code == 400