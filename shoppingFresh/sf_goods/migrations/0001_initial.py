# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('goodstitle', models.CharField(max_length=20)),
                ('goodsintro', models.CharField(max_length=100)),
                ('goodscontent', tinymce.models.HTMLField()),
                ('goodspic', models.ImageField(upload_to=b'sf_goods_pic')),
                ('goodsprice', models.DecimalField(max_digits=7, decimal_places=2)),
                ('goodsunit', models.CharField(max_length=20)),
                ('goodsstock', models.IntegerField()),
                ('goodsclick', models.IntegerField()),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typetitle', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='goodstype',
            field=models.ForeignKey(to='sf_goods.TypeInfo'),
        ),
    ]
