import pytest

from core.models import User


@pytest.mark.django_db
def test_profile(client, user_registration):

    print(user_registration)

    expected_response = {
        "id": user_registration["id"],
        "username": "username",
        # "password": "1q2w3e4r=",
        "first_name": 'Test First name',
        "last_name": 'Test Last name',
        "email": 'test@mail.com',
    }

    line = f"/core/profile"

    response = client.get(line,)
    expected_response["id"] = response.data['id']
    print(response.data)

    assert response.status_code == 200
    assert response.data == expected_response

#
# @pytest.mark.django_db
# def test_registration_request(client):
#
#     data = {
#         "username": "username",
#         "password": "ajtsntesda",
#         "password_repeat": "ajtsntesda",
#         'first_name': 'Test First name',
#         'last_name': 'Test Last name',
#         'email': 'test@mail.com',
#     }
#
#     # user = User.objects.create_user(**data)
#
#
#     expected_response = {
#         "username": "username",
#         'first_name': 'Test First name',
#         'last_name': 'Test Last name',
#         'email': 'test@mail.com',
#     }
#
#     line = f"/core/signup"
#
#     response = client.post(line, data=data)
#     expected_response["id"] = response.data['id']
#
#     assert response.status_code == 201
#     assert response.data == expected_response