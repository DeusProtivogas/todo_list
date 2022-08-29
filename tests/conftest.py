import pytest
from pytest_factoryboy import register

from tests.factories import BoardFactory, UserFactory

from todo_list.todolist import settings

pytest_plugins = "tests.fixtures"

register(UserFactory)
register(BoardFactory)



# DATABASE_URL=psql://postgres:password@localhost:5432/todolist

# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES['default'] = {
#         'ENGINE': 'postgres',
#         'HOST': 'localhost:5432',
#         'NAME': 'todolist',
#     }