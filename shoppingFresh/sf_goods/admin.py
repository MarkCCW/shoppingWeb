from django.contrib import admin
from models import *

class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'typetitle']

class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'goodstitle', 'goodsintro', 'goodscontent',
                    'goodspic', 'goodsprice', 'goodsunit', 'goodsstock',
                    'goodsclick']

admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)