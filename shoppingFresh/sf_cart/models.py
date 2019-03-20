from django.db import models

class CartInfo(models.Model):
    user = models.ForeignKey('sf_user.UserInfo')
    goods = models.ForeignKey('sf_goods.GoodsInfo')
    count = models.IntegerField()