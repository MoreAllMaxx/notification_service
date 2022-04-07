import uuid
import datetime

import pytz

from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class MobileOperatorCode(models.Model):
    code = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = 'Код мобильного оператора'
        verbose_name_plural = 'Коды мобильного оператора'


class Dispatch(models.Model):
    uid = models.UUIDField(verbose_name='Уникальный ID', default=uuid.uuid4, editable=False, unique=True,
                           primary_key=True)
    text = models.TextField(verbose_name='Текст сообщения')
    notify_date_start = models.DateTimeField(verbose_name='Дата и время запуска рассылки',)
    notify_date_end = models.DateTimeField(verbose_name='Дата и время окончания рассылки',)
    mobile_codes = models.ManyToManyField(MobileOperatorCode, verbose_name='Код мобильных операторов', max_length=50,
                                          blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)

    def __str__(self):
        return f'Рассылка {self.uid}'

    @property
    def should_send(self):
        now = timezone.now()
        return True if self.notify_date_start <= now <= self.notify_date_end else False

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Client(models.Model):
    TIMEZONE_CHOICES = list(zip(pytz.all_timezones, pytz.all_timezones))
    phone_regex = RegexValidator(
        regex=r'^7[0-9]{10}$', message="номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)"
    )
    uid = models.UUIDField(verbose_name='Уникальный ID', default=uuid.uuid4, editable=False, unique=True,
                           primary_key=True)
    phone = models.PositiveIntegerField(verbose_name='Мобильный телефон', validators=[phone_regex])
    mobile_operator_code = models.ForeignKey(MobileOperatorCode, verbose_name='Код мобильного оператора', null=True,
                                             blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)
    timezone = models.CharField(verbose_name='Часовой пояс', max_length=50, choices=TIMEZONE_CHOICES, default='UTC')

    def __str__(self):
        return f'Клиент {self.uid} с номером {self.phone}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    uid = models.UUIDField(verbose_name='Уникальный ID', default=uuid.uuid4, editable=False, unique=True,
                           primary_key=True)
    sending_date = models.DateTimeField(verbose_name='Дата отправки', auto_now_add=True)
    status = models.CharField(verbose_name='Статус отправки', max_length=15, default='В отправке')
    dispatch = models.ForeignKey(Dispatch, on_delete=models.SET_NULL, related_name='messages', null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, related_name='messages', null=True)

    def __str__(self):
        return f'Сообщение {self.uid}. Текст: {self.dispatch}. Клиент: {self.client}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
