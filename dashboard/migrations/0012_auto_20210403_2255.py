# Generated by Django 2.1.2 on 2021-04-03 22:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20210403_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='latitude',
            field=models.DecimalField(decimal_places=16, default=27.201997851500987, max_digits=19),
        ),
        migrations.AlterField(
            model_name='asset',
            name='longitude',
            field=models.DecimalField(decimal_places=16, default=77.50222119059832, max_digits=19),
        ),
        migrations.AlterField(
            model_name='asset',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 22, 55, 35, 798540)),
        ),
        migrations.AlterField(
            model_name='trip',
            name='startTime',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 22, 55, 35, 800540)),
        ),
        migrations.AlterField(
            model_name='trip',
            name='time',
            field=models.DecimalField(decimal_places=4, max_digits=12, null=True),
        ),
    ]
