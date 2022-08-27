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

    category = response.data

    data_goal = {
        "title": "Test goal",
        "description": "Test desc",
        "category": category["id"],
    }


    response = client.post("/goals/goal/create", data=data_goal)

    assert response.status_code == 201
    # assert response.data["title"] == data_category["title"]
    # assert response.data["board"] == board["id"]