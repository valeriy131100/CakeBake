# Сервис продажи тортов CakeBake

Создай и закажи торт на свой вкус!

## Запуск

Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub. Установите зависимости:

```sh
pip install -r requirements.txt
```

Создайте базу данных

```sh
python3 manage.py migrate
```

Запустите сервер разработки

```
python3 manage.py runserver
```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения.
Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

### Доступные переменные:
- `DEBUG` — режим отладки. Поставьте `True`, чтобы увидеть отладочную информацию в случае ошибки.
- `SECRET_KEY` — секретный ключ проекта
- `ALLOWED_HOSTS` — см [документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- `DATABASE_URL` — см [здесь](https://github.com/kennethreitz/dj-database-url#url-schema)

#### Настройки приема платежей через yookassa
- `YOOKASSA_ACCOUNT_ID` 
- `YOOKASSA_SECRET_KEY`

#### Настройки отправки почты
По умолчанию используется SMTP бэкенд (https://docs.djangoproject.com/en/4.0/topics/email/#smtp-backend)

- `EMAIL_BACKEND` — бэкенд, по умолчанию — `django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST` — сервер, например, для gmail:`smtp.gmail.com`
- `EMAIL_PORT` — порт, по умолчанию `587`
- `EMAIL_USE_TLS` — использовать TLS соединение, `true`
- `EMAIL_HOST_USER` — почтовый адрес для отправки почты: `username@host.com`
- `EMAIL_HOST_PASSWORD` — секретный пароль для приложения, как получить: https://dev.to/abderrahmanemustapha/how-to-send-email-with-django-and-gmail-in-production-the-right-way-24ab