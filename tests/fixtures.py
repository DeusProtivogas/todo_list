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



@pytest.fixture
@pytest.mark.django_db
def user_registration(client, django_user_model):
    username = "username"
    password = "1q2w3e4r="
    first_name = 'Test First name'
    last_name = 'Test Last name'
    email = 'test@mail.com'


    django_user_model.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
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