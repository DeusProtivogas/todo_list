from collections import OrderedDict

import pytest

from goals.models import Board
from core.models import User
from goals.models import BoardParticipant


@pytest.mark.django_db
def test_board_get(client, user_token):
    data = {
        "title": "Test",
    }

    board = Board.objects.create(**data)
    user = User.objects.get(pk=user_token["id"])
    board_part = BoardParticipant.objects.create(
        board_id=board.pk,
        user_id=user.pk,
        role=1,
    )
    board.participants.set([board_part])
    # print(board.participants)

    expected_response = {
        'id': board.pk,
        'participants': [OrderedDict([
            ('id', board_part.pk),
            ('role', 1),
            ('user', 'user_name'),
            ('created', board_part.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            ('updated', board_part.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            ('board', board.pk)
        ])],
        'created': board.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        'updated': board.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        'title': 'Test',
        'is_deleted': False}

    btest = Board.objects.all()
    # print(btest)
    board_created = client.get(f"/goals/board/{board.pk}")
    # print(board_created.status_code)
    # print(board_created.data)

    assert board_created.status_code == 200
    assert board_created.data == expected_response



@pytest.mark.django_db
def test_board_bad_get(client, user_token):

    response = client.get("/goals/board/123" )

    assert response.status_code == 404
