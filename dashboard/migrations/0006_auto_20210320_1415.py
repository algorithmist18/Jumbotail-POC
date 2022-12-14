# Generated by Django 3.1.7 on 2021-03-20 08:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20210320_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='latitude',
            field=models.DecimalField(decimal_places=16, default=27.20827808660063, max_digits=19),
        ),
        migrations.AlterField(
            model_name='asset',
            name='longitude',
            field=models.DecimalField(decimal_places=16, default=77.49834174865067, max_digits=19),
        ),
        migrations.AlterField(
            model_name='asset',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 20, 14, 15, 7, 334803)),
        ),
    ]
