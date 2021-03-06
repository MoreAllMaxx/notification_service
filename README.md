Сервис уведомления

Сделайте следующее для запуска приложения:

Добавьте файл settings.py в папку service/service/, скопировав все из файла settings.py.default, добавить SECRET KEY.

Создайте виртуальной окружение (по желанию):

`python -m venv venv`

Установите необходимые модули для работы с приложением:

`pip install -r requirements.txt`

Перейдите в папку service/

`cd service/`

Выполните команду migrate:

`python manage.py migrate`

Запустите сервер:

`python manage.py runserver`

И запустите сервис для отправки сообщений (вторым терминалом):

`python manage.py send_messages`

_Для корректной работы сервиса локально установите RabbitMQ_

По адресу http://127.0.0.1:8000/api/ :

1. Создайте Тег (или несколько Тегов)
2. Создайте Клиента (Клиентов)
3. Создайте Рассылку (Рассылки)
4. Создайте Сообщение (Сообщения)

Созданные в API сообщения будут автоматически переданы на указанный в settings.py URL_CLIENT
между датами, указанными в Клиенте.

По адресу http://127.0.0.1:8000/docs/ Вы можете увидеть документацию на API (swagger)