from collections import OrderedDict

import pytest


# @pytest.mark.django_db
# def test_goal_list(client, user_token):
#
#     line = f"/goals/goal/list"
#
#     response = client.get(line)#, HTTP_AUTHORIZATION="Token " + user_token)
#
#     assert response.status_code == 200
#     assert response.data == []
from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory, Goal


@pytest.mark.django_db
def test_goal_list(client, user_token):

    data_board = {
        "title": "Test board",
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

    goal_1 = Goal.objects.create(
        title="Test goal",
        category=category,
        user=user,
    )
    print(goal_1)
    goal_2 = Goal.objects.create(
        title="Test goal",
        category=category,
        user=user,
    )
    print(goal_2)

    goals = client.get(f"/goals/goal/list")
    print(goals.data)

    expected_response = [OrderedDict([
            ('id', goal_1.pk),
            ('user', OrderedDict([
                ('id', user.pk),
                ('username', 'user_name'),
                ('first_name', ''),
                ('last_name', ''),
                ('email', '')])),
            ('created', goal_1.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
            ('updated', goal_1.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
            ('title', 'Test goal'),
            ('description', ''),
            ('due_date', None),
            ('status', 1),
            ('priority', 2),
            ('category', 3)]),
        OrderedDict([
            ('id', goal_2.pk),
            ('user', OrderedDict([
                ('id', user.pk),
                ('username', 'user_name'),
                ('first_name', ''),
                ('last_name', ''),
                ('email', '')])),
            ('created', goal_2.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
            ('updated', goal_2.updated.strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
            ('title', 'Test goal'),
            ('description', ''),
            ('due_date', None),
            ('status', 1),
            ('priority', 2),
            ('category', 3)])
    ]


    assert goals.status_code == 200
    assert goals.data == expected_response