from collections import OrderedDict

import pytest

from goals.models import Board, BoardParticipant

from core.models import User

@pytest.mark.django_db
def test_board_create(client, user_token):
    """
    Создание доски, авторизованный пользователь
    """

    data = {
        "title": "Test",
    }


    response = client.post("/goals/board/create", data=data)

    expected_response = {
        "id": response.data["id"],
        "title": "Test",
        "is_deleted": False,
        "created": response.data["created"],
        "updated": response.data["updated"],
    }


    assert response.status_code == 201
    assert expected_response == response.data


#
# @pytest.mark.django_db
# def test_board_create(client, user_token):
#     """
#     Создание доски, авторизованный пользователь
#     """
#
#
#     data = {
#         "title": "Test",
#     }
#
#     board = Board.objects.create(**data)
#     user = User.objects.get(pk=user_token["id"])
#     board_part = BoardParticipant.objects.create(
#         board_id=board.pk,
#         user_id=user.pk,
#         role=1,
#     )
#     board.participants.set([board_part])
#     print(board.participants)
#
#     expected_response = {
#         'id': 1,
#         'participants': [OrderedDict([
#             ('id', 1),
#             ('role', 1),
#             ('user', 'user_name'),
#             ('created', board_part.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
#             ('updated', board_part.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
#             ('board', 1)
#         ])],
#         'created': board.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#         'updated': board.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
#         'title': 'Test',
#         'is_deleted': False}
#
#     btest = Board.objects.all()
#     print(btest)
#     board_created = client.get(f"/goals/board/{board.pk}")
#     print(board_created.status_code)
#     print(board_created.data)
#
#
#     assert board_created.status_code == 200
#     assert board_created.data == expected_response


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