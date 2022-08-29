from collections import OrderedDict

import pytest

from goals.models import Board


# @pytest.mark.django_db
# def test_board_list(client, user_token):
#     """
#     Получение списка досок, сравнение с ожидаемым
#     """
#     data_1 = {
#         "title": "Test1",
#     }
#     response_1 = client.post("/goals/board/create", data=data_1)
#     board_1 = response_1.data
#     data_2 = {
#         "title": "Test2",
#     }
#     response_2 = client.post("/goals/board/create", data=data_2)
#     board_2 = response_2.data
#
#     expected_response = [
#        OrderedDict(board_1), OrderedDict(board_2)
#     ]
#
#     response = client.get("/goals/board/list")
#     # for resp in response.data:
#     #     resp.data.pop("participants")
#
#     assert response.status_code == 200
#     assert response.data == expected_response
from core.models import User
from goals.models import BoardParticipant


@pytest.mark.django_db
def test_board_get(client, user_token):
    data_1 = {
        "title": "Test1",
    }

    board_1 = Board.objects.create(**data_1)
    user = User.objects.get(pk=user_token["id"])
    board_part = BoardParticipant.objects.create(
        board_id=board_1.pk,
        user_id=user.pk,
        role=1,
    )
    board_1.participants.set([board_part])
    # print(board.participants)

    data_2 = {
        "title": "Test2",
    }

    board_2 = Board.objects.create(**data_2)
    user = User.objects.get(pk=user_token["id"])
    board_part = BoardParticipant.objects.create(
        board_id=board_2.pk,
        user_id=user.pk,
        role=1,
    )
    board_2.participants.set([board_part])
    # print(board.participants)

    expected_response = [
        OrderedDict([
            ('id', board_1.pk),
            ('created', board_1.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            ('updated', board_1.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            ('title', 'Test1'),
            ('is_deleted', False)
        ]),
        OrderedDict([
            ('id', board_2.pk),
            ('created', board_2.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            ('updated', board_2.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            ('title', 'Test2'),
            ('is_deleted', False)])
    ]



    boards = client.get(f"/goals/board/list")
    # print(boards.status_code)
    # print(boards.data)

    assert boards.status_code == 200
    assert boards.data == expected_response