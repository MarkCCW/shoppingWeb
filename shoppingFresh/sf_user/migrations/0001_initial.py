# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('userpwd', models.CharField(max_length=40)),
                ('useremail', models.CharField(max_length=30)),
                ('userreceiver', models.CharField(max_length=20)),
                ('userphone', models.CharField(max_length=10)),
            ],
        ),
    ]
