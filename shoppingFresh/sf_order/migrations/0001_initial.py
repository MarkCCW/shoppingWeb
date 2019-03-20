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
            name='OrderDetailInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='sf_goods.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('orderid', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('orderdate', models.DateTimeField(auto_now=True)),
                ('orderaddress', models.CharField(max_length=100)),
                ('ordertotal', models.DecimalField(max_digits=7, decimal_places=2)),
                ('orderIsPay', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to='sf_user.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(to='sf_order.OrderInfo'),
        ),
    ]
