import requests
from celery.task import task
from django.conf import settings

URL = settings.SERVICE_URL


@task(bind=True, max_retries=25, default_retry_delay=10)
def url_post(message_id, header, data):
    try:
        response = requests.post(url=(URL + message_id), headers=header, json=data)
    except ConnectionError:
        return f'Ошибка соединения'
