# Generated by Django 3.2 on 2022-04-07 10:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatch',
            name='notify_date_end',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 19, 26, 50, 598066), verbose_name='Дата и время окончания рассылки'),
        ),
        migrations.AlterField(
            model_name='dispatch',
            name='notify_date_start',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 7, 15, 26, 50, 598066), verbose_name='Дата и время запуска рассылки'),
        ),
    ]