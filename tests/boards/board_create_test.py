import pytest


@pytest.mark.django_db
def test_board_create(client, user_token):
    """
    Создание доски, авторизованный пользователь
    """

    data = {
        "title": "Test",
    }

    response = client.post("/goals/board/create", data=data)
    board_created = client.get("/goals/board/" + str(response.data["id"]))
    board_created.data.pop("participants")


    assert response.status_code == 201
    assert board_created.data == response.data


@pytest.mark.django_db
def test_board_bad_create(client, user_token):
    """
    Создание доски с неправильным заголовком
    """
    data = {
        "title": "",
    }

    response = client.post("/goals/board/create", data=data)


    assert response.status_code == 400



@pytest.mark.django_db
def test_board_unauthorized_create(client):
    """
    Создание доски, неавторизованный пользователь
    """

    data = {
        "title": "Title",
    }

    response = client.post("/goals/board/create", data=data)


    assert response.status_code == 403