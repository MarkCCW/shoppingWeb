# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sf_user', '0002_auto_20190305_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='userphone',
            field=models.CharField(default=b'', max_length=10),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='userreceiver',
            field=models.CharField(default=b'', max_length=20),
        ),
    ]
