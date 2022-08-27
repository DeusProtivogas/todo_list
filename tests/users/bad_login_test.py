import pytest


@pytest.mark.django_db
def test_bad_login(client):

    data = {
        "username": "Fake_name",
        "password": "badpassword1",
    }

    line = f"/core/login"

    response = client.post(line, data=data)

    assert response.status_code == 400