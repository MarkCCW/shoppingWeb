from django.db import models

class OrderInfo(models.Model):
    orderid = models.CharField(max_length=20, primary_key=True)
    orderdate = models.DateTimeField(auto_now=True)
    orderaddress = models.CharField(max_length=100)
    ordertotal = models.DecimalField(max_digits=7, decimal_places=2)
    orderIsPay = models.BooleanField(default=False)
    user = models.ForeignKey('sf_user.UserInfo')

class OrderDetailInfo(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=2)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2)
    count = models.IntegerField()
    goods = models.ForeignKey('sf_goods.GoodsInfo')
    order = models.ForeignKey(OrderInfo)
