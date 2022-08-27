import pytest


@pytest.mark.django_db
def test_board_list(client, user_token):

    line = f"/goals/board/list"

    response = client.get(line)#, HTTP_AUTHORIZATION="Token " + user_token)

    assert response.status_code == 200
    assert response.data == []