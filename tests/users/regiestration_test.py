import pytest



@pytest.mark.django_db
def test_registration(client):

    data = {
        "username": "username",
        "password": "ajtsntesda",
        "password_repeat": "ajtsntesda",
        'first_name': 'Test First name',
        'last_name': 'Test Last name',
        'email': 'test@mail.com',
    }

    # user = User.objects.create_user(**data)


    expected_response = {
        "username": "username",
        'first_name': 'Test First name',
        'last_name': 'Test Last name',
        'email': 'test@mail.com',
    }

    line = f"/core/signup"

    response = client.post(line, data=data)
    expected_response["id"] = response.data['id']

    assert response.status_code == 201
    assert response.data == expected_response