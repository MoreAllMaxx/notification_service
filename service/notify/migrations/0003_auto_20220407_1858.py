# Generated by Django 3.2 on 2022-04-07 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0002_auto_20220407_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dispatch',
            name='notify_date_end',
            field=models.DateTimeField(verbose_name='Дата и время окончания рассылки'),
        ),
        migrations.AlterField(
            model_name='dispatch',
            name='notify_date_start',
            field=models.DateTimeField(verbose_name='Дата и время запуска рассылки'),
        ),
    ]
