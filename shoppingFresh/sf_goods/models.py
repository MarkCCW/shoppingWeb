from django.db import models
from tinymce.models import HTMLField

class TypeInfo(models.Model):
    typetitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.typetitle.encode('utf-8')

class GoodsInfo(models.Model):
    goodstitle = models.CharField(max_length=20)
    goodsintro = models.CharField(max_length=100)
    goodscontent = HTMLField()
    goodspic = models.ImageField(upload_to='sf_goods_pic')
    goodsprice = models.DecimalField(max_digits=7, decimal_places=2)
    goodsunit = models.CharField(max_length=20)
    goodsstock = models.IntegerField()
    goodsclick = models.IntegerField()
    isDelete = models.BooleanField(default=False)
    goodstype = models.ForeignKey(TypeInfo)

    def __str__(self):
        return self.goodstitle.encode('utf-8')
