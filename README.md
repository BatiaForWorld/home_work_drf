# Django REST Framework

Домашнее задание на тему:

### Вьюсеты и дженерики (viewsets and generics)

и

### Сериализаторы

Для установки проекта создайте проект и импортируйте его по ссылке github

Создайте виртуальное окружение

```bash
python3.13 -m venv .venv
```

Установите зависимости из файла requirements.txt

```bash
pip install -r requirements.txt
```

Заполните файл .env по примеру env.example, указав данные для соединения с БД postgreSQL.

Выполните миграции

```bash
python3 manage.py migrate
```

Загрузите фикстуры для заполнения БД

```bash
python3 manage.py loaddata users/fixtures/users.json
python3 manage.py loaddata courses/fixtures/courses.json
python3 manage.py loaddata courses/fixtures/lessons.json
python3 manage.py loaddata users/fixtures/payments.json
```

Скачайте [Postman](https://dl.pstmn.io/download/latest/linux_64) для вашего дистрибутива Linux, распакуйте в удобную для
вас папку и запустите


Автор: Казанцев Андрей




