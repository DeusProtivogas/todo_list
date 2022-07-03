# Project description

# TODO list: Календарь для планирования задач название

# Стек (python3.9, Django, Postgres)

# как запустить (установить зависимости, заполнить .env + какими значениями, накатить миграции, запустить проект)

Установка зависимостей:

pip install -r requirements.txt

.env:

DEBUG: True, если идет разработка
SECRET_KEY: Строка с екретным ключем
DATABASE_URL: информация про бд

Миграции для бд:
python3 manage.py makemigrations
python3 manage.py migrate

Запуск:
python3 manage.py runserver
