# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sf_goods', '0001_initial'),
        ('sf_user', '0003_auto_20190306_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='sf_goods.GoodsInfo')),
                ('user', models.ForeignKey(to='sf_user.UserInfo')),
            ],
        ),
    ]
