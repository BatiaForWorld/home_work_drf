# Django REST Framework

Домашнее задание на тему:

### Вьюсеты и дженерики (viewsets and generics)

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
Также заполните тестовые настройки Stripe:
- `STRIPE_SECRET_KEY`
- `STRIPE_SUCCESS_URL`
- `STRIPE_CANCEL_URL`

Выполните миграции

```bash
python3 manage.py migrate
```

Скачайте [Postman](https://dl.pstmn.io/download/latest/linux_64) для вашего дистрибутива Linux, распакуйте в удобную для
вас папку и запустите

# Права доступа в DRF 
## JWT

### Фикстуры
Для добавления группы модераторов используйте фикстуру [users/fixtures/groups.json](users/fixtures/groups.json).

Пример применения:

```bash
python3 manage.py loaddata users/fixtures/groups.json
```
Создайте администратора:
```commandline
python3 manage.py createsuperuser
```
После загрузки фикстуры назначайте пользователей в группу moderators через админ-панель.

### Возможности проекта
- Регистрация пользователей и JWT-аутентификация.
- CRUD для пользователей (публичный и полный профиль в зависимости от владельца).
- CRUD для курсов и уроков.
- Разграничение прав: модераторы могут просматривать и редактировать любые курсы и уроки, но не создавать и не удалять.
- Пользователи, не входящие в группу модераторов, видят и изменяют только свои курсы и уроки.

# Валидаторы, пагинация и тесты

Для сохранения уроков и курсов реализована дополнительная проверка на отсутствие в материалах ссылок на сторонние ресурсы, 
кроме youtube.com.
То есть ссылки на видео можно прикреплять в материалы, 
а ссылки на сторонние образовательные платформы или личные сайты — нельзя.

Добавлена модель подписки на обновления курса для пользователя. 

Реализован эндпоинт для установки подписки пользователя и на удаление подписки у пользователя.

Реализована пагинация для вывода всех уроков и курсов.

Реализована документация API через Swagger и Redoc.

Реализована интеграция оплаты курсов через Stripe Checkout.

Написаны тесты, которые проверяют корректность работы CRUD уроков и функционал работы подписки на обновления курса.

Сохранены результат проверки покрытия тестами.

### Что бы запустить тесты введите команду:

```commandline
python3 manage.py test
```

### Чтобы сохранить отчет о покрытии тестами в определенную папку, например, в папку htgmlcov,
нужно выполнить следующие шаги:

Запустить тесты только для ****courses****, выполните:

```commandline
python manage.py test courses
```
Отчёт о покрытии:

```commandline
coverage report
```

Запустить тесты с подсчетом покрытия:

```commandline
coverage run --source='.' manage.py test
```

Сохранить отчет в папку htgmlcov:

```commandline
coverage html -d htgmlcov
```

## Документация API

- Swagger UI: `/swagger/`
- OpenAPI JSON/YAML: `/swagger<format>/`
- ReDoc: `/redoc/`

## Оплата Stripe

Эндпоинты:
- `GET /users/payments/` — список платежей пользователя (модератор видит все).
- `POST /users/payments/create/` — создать платеж и получить ссылку на оплату (`payment_link`).
- `GET /users/payments/status/<stripe_session_id>/` — проверить `payment_status` сессии в Stripe.

При создании платежа система автоматически создаёт в Stripe:
- Product
- Price (сумма передаётся в копейках)
- Checkout Session

Взаимодействие со Stripe вынесено в сервисные функции приложения `users`.

В `.env` укажите реальные URL редиректа, а не заглушки:
- `STRIPE_SUCCESS_URL=http://localhost:8000/users/payments/success/?session_id={CHECKOUT_SESSION_ID}`
- `STRIPE_CANCEL_URL=http://localhost:8000/users/payments/cancel/`

## Полный сценарий запросов (curl)

Ниже минимальный рабочий сценарий от регистрации до получения ссылки Stripe.

1) Регистрация (без Authorization):

```bash
curl -X POST http://localhost:8000/users/register/ \
	-H "Content-Type: application/json" \
	-d '{
		"email": "vasia@example.com",
		"password1": "vasia12345",
		"password2": "vasia12345"
	}'
```

2) Логин (без Authorization):

```bash
curl -X POST http://localhost:8000/users/login/ \
	-H "Content-Type: application/json" \
	-d '{
		"email": "vasia@example.com",
		"password": "vasia12345"
	}'
```

3) Обновить access по refresh:

```bash
curl -X POST http://localhost:8000/users/token/refresh/ \
	-H "Content-Type: application/json" \
	-d '{
		"refresh": "<YOUR_REFRESH_TOKEN>"
	}'
```

4) Создать курс с ценой (нужен для оплаты):

```bash
curl -X POST http://localhost:8000/courses/ \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
	-d '{
		"title": "Python Pro",
		"description": "Оплачиваемый курс",
		"price": 500
	}'
```

5) Создать платеж и получить `payment_link` Stripe:

```bash
curl -X POST http://localhost:8000/users/payments/create/ \
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
	-d '{
		"course": 1
	}'
```

6) Получить список своих платежей:

```bash
curl -X GET http://localhost:8000/users/payments/ \
	-H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

7) Проверить статус платежа по `stripe_session_id`:

```bash
curl -X GET http://localhost:8000/users/payments/status/cs_test_123/ \
	-H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

Если приходит `token_not_valid` или `Token is expired`:
- получите новый `access` через `/users/token/refresh/`;
- или заново войдите через `/users/login/`.
- убедитесь, что на `/users/register/` и `/users/login/` вы не отправляете старый `Authorization`.


Автор: Казанцев Андрей




