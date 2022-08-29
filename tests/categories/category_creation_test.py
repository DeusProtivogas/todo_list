from collections import OrderedDict

import pytest

from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory


@pytest.mark.django_db
def test_category_create(client, user_token):

    data_board = {
        "title": "Test",
    }

    board = Board.objects.create(**data_board)
    user = User.objects.get(pk=user_token["id"])
    board_part = BoardParticipant.objects.create(
        board_id=board.pk,
        user_id=user.pk,
        role=1,
    )
    board.participants.set([board_part])


    data_category = {
        "title": "Test category",
        "board": board,
        "user": user,
    }

    category = GoalCategory.objects.create(**data_category)

    expected_response = {
        "id": category.pk,
        "created": category.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "updated": category.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "title": "Test category",
        "is_deleted": False,
        "board": board.pk,
        "user": OrderedDict([
            ('id', user.pk),
            ('username', 'user_name'),
            ('first_name', ''),
            ('last_name', ''),
            ('email', "")
        ]),
    }

    response = client.get(f"/goals/goal_category/{category.pk}")

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_category_create_bad_name(client, user_token):
    data_board = {
        "title": "Test",
    }

    board = Board.objects.create(**data_board)
    user = User.objects.get(pk=user_token["id"])
    board_part = BoardParticipant.objects.create(
        board_id=board.pk,
        user_id=user.pk,
        role=1,
    )
    board.participants.set([board_part])


    data_category = {
            "title": "",
            "board": board.pk,
        }


    response = client.post("/goals/goal_category/create", data=data_category)

    assert response.status_code == 400


@pytest.mark.django_db
def test_category_create_bad_board(client, user_token):
    data_board = {
        "title": "Test",
    }

    board = Board.objects.create(**data_board)
    user = User.objects.get(pk=user_token["id"])
    board_part = BoardParticipant.objects.create(
        board_id=board.pk,
        user_id=user.pk,
        role=1,
    )
    board.participants.set([board_part])


    data_category = {
        "title": "Test category",
        "board": board.pk + 1,
    }


    response = client.post("/goals/goal_category/create", data=data_category)

    assert response.status_code == 400
