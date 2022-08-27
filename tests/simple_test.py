from django.http import HttpResponseNotFound


def test_root_not_found(client):
    response: HttpResponseNotFound = client.get("/")

    assert response.status_code == 404