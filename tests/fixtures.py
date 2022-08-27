import pytest


@pytest.fixture
@pytest.mark.django_db
def user_token(client, django_user_model):
    username = "user_name"
    password = "1q2w3e4r="

    django_user_model.objects.create_user(
        username=username, password=password,
    )

    response = client.post(
        "/core/login",
        {
            "username": username,
            "password": password,
        },
        format="json",
    )

    # print(response.data)
    # print("Fixture: " + response.data[0])

    return response.data