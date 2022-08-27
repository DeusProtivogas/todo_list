import pytest


@pytest.mark.django_db
def test_bad_registration(client):
    data = {

    }

    line = f"/core/signup"

    response = client.post(line, data=data)

    assert response.status_code == 400
    assert response.data["username"][0].title() == "This Field Is Required."
    assert response.data["password"][0].title() == "This Field Is Required."
    assert response.data["password_repeat"][0].title() == "This Field Is Required."


@pytest.mark.django_db
def test_bad_registration_username(client):
    data = {
        "username": "Bad username",
        "password": "1q2w3e4r=",
        "password_repeat": "1q2w3e4r=",
    }



    line = f"/core/signup"

    response = client.post(line, data=data)

    assert response.status_code == 400
    assert response.data["username"][0].title() == "Enter A Valid Username. This Value May Contain Only Letters, " \
                                                   "Numbers, And @/./+/-/_ Characters."



@pytest.mark.django_db
def test_bad_registration_short_password(client):
    data = {
        "username": "username",
        "password": "1",
        "password_repeat": "1",
    }



    line = f"/core/signup"

    response = client.post(line, data=data)

    assert response.status_code == 400
    assert response.data["password"][0].title() == "This Password Is Too Short. It Must Contain At Least 8 Characters."


@pytest.mark.django_db
def test_bad_registration_common_password(client):
    data = {
        "username": "username",
        "password": "12345678",
        "password_repeat": "12345678",
    }

    expected_response = {
        # "username":
    }

    line = f"/core/signup"

    response = client.post(line, data=data)

    assert response.status_code == 400
    assert response.data["password"][0].title() == "This Password Is Too Common."


@pytest.mark.django_db
def test_bad_registration_incompatible_passwords(client):
    data = {
        "username": "username",
        "password": "ajtsntesda",
        "password_repeat": "someOtherPassword",
    }



    line = f"/core/signup"

    response = client.post(line, data=data)

    assert response.status_code == 400
    assert response.data["non_field_errors"][0].title() == "Password And Password_Repeat Is Not Equal"

@pytest.mark.django_db
def test_bad_registration_incorrect_email(client):
    data = {
        "username": "username",
        "email": "badEmail",
        "password": "ajtsntesda",
        "password_repeat": "ajtsntesda",
    }



    line = f"/core/signup"

    response = client.post(line, data=data)

    assert response.status_code == 400
    assert response.data["email"][0].title() == "Enter A Valid Email Address."



@pytest.mark.django_db
def test_bad_registration_same_username(client):

    data_1 = {
        "username": "username",
        "password": "ajtsntesda",
        "password_repeat": "ajtsntesda",
    }

    data_2 = {
        "username": "username",
        "password": "ajtsntesda",
        "password_repeat": "ajtsntesda",
    }

    line = f"/core/signup"

    response_1 = client.post(line, data=data_1)
    response_2 = client.post(line, data=data_2)


    assert response_2.status_code == 400
    assert response_2.data['username'][0].title() == "A User With That Username Already Exists."