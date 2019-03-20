# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sf_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='useraddress',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='userpostalcode',
            field=models.CharField(default=b'', max_length=5),
        ),
    ]
