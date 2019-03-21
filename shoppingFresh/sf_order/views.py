# coding:utf-8
from django.shortcuts import render, redirect
from sf_user.models import UserInfo
from sf_cart.models import CartInfo
from .models import *
from sf_user import user_decorator
from datetime import datetime
from django.db import transaction


@user_decorator.login
def order(request):
    # 查詢用戶
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 根據提交,查詢購物車資訊
    get = request.GET
    cart_ids = get.getlist("cart_id")
    cart_ids_list = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids_list)

    context = {
        'title': '提交訂單',
        'page_name': 1,
        'carts': carts,
        'cart_ids': ','.join(cart_ids),
        'user': user,
    }
    return render(request, 'sf_order/place_order.html', context)


# 使用事務功能,處理訂單操作

@user_decorator.login
def order_handle(request):
    # 創建回歸點
    point = transaction.savepoint()
    # 購物車編號
    cart_ids = request.POST.get("cart_ids")
    try:
        order = OrderInfo()
        now = datetime.now()
        userid = request.session['user_id']
        order.orderid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), userid)
        order.user_id = userid
        order.orderdate = now
        print request.POST.get('receiver_info')
        order.orderaddress = request.POST.get('receiver_info')
        order.ordertotal = 0
        order.save()

        cart_ids = [int(item) for item in cart_ids.split(',')]
        print cart_ids
        total_money = 0

        for id1 in cart_ids:
            detail = OrderDetailInfo()
            detail.order = order

            # 查詢購物車
            cart = CartInfo.objects.get(id=id1)
            # 判斷商品庫存
            goods = cart.goods
            # 庫存大於購物車數量
            if goods.goodsstock >= cart.count:
                goods.goodsstock = cart.goods.goodsstock - cart.count
                goods.save()

                detail.goods_id = goods.id

                price = goods.goodsprice
                detail.price = price
                count = cart.count
                detail.count = count
                detail.subtotal = price*count
                detail.save()
                total_money = total_money + price*count
                # 刪除購物車數據
                cart.delete()
            else:
                # 如果庫存少於購買數量,操作失敗
                transaction.savepoint_rollback(point)
                return redirect('/cart/')
        # 操作成功
        order.ordertotal = total_money + 100
        order.save()
        transaction.savepoint_commit(point)
        
    except Exception as e:
        print '================%s'%e
        transaction.savepoint_rollback(point)
        
    return redirect('/user/order/')


@user_decorator.login
def pay(request, order_id):
    order = OrderInfo.objects.get(orderid=order_id)
    order.orderIsPay = True
    order.save()
    context = {'order': order}

    return render(request, 'sf_order/pay.html', context)
