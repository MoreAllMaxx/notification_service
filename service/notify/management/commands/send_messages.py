import logging
import os
import time

import requests
from django.conf import settings
from django.core.management import BaseCommand
# from .tasks import url_post
from django.db.models import Q

from .tasks import url_post
from notify.models import Client, Message, Dispatch


TOKEN = settings.SERVICE_TOKEN
logger = logging.getLogger('notification service')


def configure_logging(log):

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M'))
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler(os.path.join('notify', 'management', 'commands', 'notification service.log'),
                                       encoding='utf8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M'))
    file_handler.setLevel(logging.INFO)

    if log.hasHandlers():
        log.handlers.clear()

    log.addHandler(stream_handler)
    log.addHandler(file_handler)

    log.setLevel(logging.INFO)


configure_logging(logger)


def get_messages():

    header = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    mailing = [obj for obj in Dispatch.objects.all() if obj.should_send]
    for mail in mailing:
        client_query = Q(mobile_operator_code__in=[obj.id for obj in mail.mobile_codes.all()])
        client_query.add(Q(tags__in=[obj.id for obj in mail.tags.all()]), Q.AND)
        clients = Client.objects.filter(client_query)
        for client in clients:
            messages = Message.objects.filter(status__in=['В отправке', 'Не отправлено']).select_related(
                'client', 'dispatch').all()
            for message in messages:
                data = {
                    'id': str(message.uid),
                    "phone": client.phone,
                    "text": mail.text
                }
                try:
                    url_post(message_id=str(message.uid), header=header, data=data)
                except Exception as exc:
                    logger.info(f'Сообщение {message} не отправлено. Текст: {mail.text}. Ошибка {exc}')
                    message.status = 'Не отправлено'
                    message.save()
                else:
                    logger.info(f'Сообщение {message} отправлено. Текст: {mail.text}')
                    message.status = 'Отправлено'
                    message.save()

    time.sleep(5)


class Command(BaseCommand):
    help = 'Отправить сообщение на внешний сервис'

    def handle(self, *args, **options):
        while True:
            try:
                get_messages()
            except Exception as exc:
                logger.info(f'Ошибка {exc}')
