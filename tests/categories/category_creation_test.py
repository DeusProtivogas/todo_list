import pytest


@pytest.mark.django_db
def test_category_create(client, user_token):

    data_board = {
        "title": "Test",
    }

    response = client.post("/goals/board/create", data=data_board)

    board = response.data

    data_category = {
        "title": "Test category",
        "board": board["id"],
    }

    response = client.post("/goals/goal_category/create", data=data_category)

    assert response.status_code == 201
    assert response.data["title"] == data_category["title"]
    assert response.data["board"] == board["id"]



@pytest.mark.django_db
def test_category_create_bad_name(client, user_token):

    data_board = {
        "title": "Test",
    }

    response = client.post("/goals/board/create", data=data_board)


    board = response.data

    data_category = {
        "title": "",
        "board": board["id"],
    }


    response = client.post("/goals/goal_category/create", data=data_category)

    assert response.status_code == 400


@pytest.mark.django_db
def test_category_create_bad_board(client, user_token):

    data_board = {
        "title": "Test",
    }

    response = client.post("/goals/board/create", data=data_board)


    board = response.data

    data_category = {
        "title": "Test category",
        "board": board["id"] + 1,
    }


    response = client.post("/goals/goal_category/create", data=data_category)

    assert response.status_code == 400
