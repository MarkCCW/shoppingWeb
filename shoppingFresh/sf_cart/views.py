# coding:utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from sf_user import user_decorator
from .models import *


# 購物車頁面
@user_decorator.login
def cart(request):
    user_id = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=user_id)
    context = {
        'title': '購物車',
        'page_name': 1,
        'carts': carts,
    }
    return render(request, 'sf_cart/cart.html', context)


# 新增購物車
@user_decorator.login
def add(request, goods_id, count):
    user_id = request.session['user_id']
    goods_id = int(goods_id)
    count = int(count)

    # 查詢購物車是否已有此商品,如果有則數量增加,如果沒有則新增
    carts = CartInfo.objects.filter(user_id=user_id, goods_id=goods_id)
    if len(carts) >= 1:
        cart = carts[0]
        cart.count += count

    else:
        cart = CartInfo()
        cart.user_id = user_id
        cart.goods_id = goods_id
        cart.count = count
    cart.save()

    # 判斷是否為Ajax請求
    if request.is_ajax():
        count_of_cart = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'cart_id': cart.id, 'count_of_cart': count_of_cart, 'goods_id':goods_id})

    else:
        return redirect('/cart/')


@user_decorator.login
def edit(request, cart_id, count):
    count_now = 1
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        count_now = cart.count
        cart.count = int(count)
        cart.save()
        data = {'result': 0}

    except Exception as e:
        data = {'result': count_now}

    return JsonResponse(data)

@user_decorator.login
def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'result': 1}

    except Exception as e:
        data = {'result': 0}

    return JsonResponse(data)