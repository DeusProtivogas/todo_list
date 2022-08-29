import factory

from goals.models import Board
from core.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "username"
    password = "1q2w3e4r="



class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = "Test board"
    participants = []
