from collections import OrderedDict

import pytest

from goals.models import Board


@pytest.mark.django_db
def test_board_list(client, user_token):
    """
    Получение списка досок, сравнение с ожидаемым
    """
    data_1 = {
        "title": "Test1",
    }
    response_1 = client.post("/goals/board/create", data=data_1)
    board_1 = response_1.data
    data_2 = {
        "title": "Test2",
    }
    response_2 = client.post("/goals/board/create", data=data_2)
    board_2 = response_2.data

    expected_response = [
       OrderedDict(board_1), OrderedDict(board_2)
    ]

    response = client.get("/goals/board/list")
    # for resp in response.data:
    #     resp.data.pop("participants")

    assert response.status_code == 200
    assert response.data == expected_response
