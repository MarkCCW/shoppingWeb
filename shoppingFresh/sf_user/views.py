# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from sf_goods.models import *
from sf_order.models import *
from models import *
from hashlib import sha1
from . import user_decorator

# 用戶註冊
def register(request):
    context = {'title': '用戶註冊'}
    return render(request, 'sf_user/register.html', context)

# 接收用戶註冊請求
def register_handle(request):
    post = request.POST
    username = post.get('user_name')
    userpwd = post.get('pwd')
    usercheckpwd = post.get('cpwd')
    useremail = post.get('email')

    # 檢查用戶密碼
    if userpwd != usercheckpwd:
        return redirect('/user/register/')

    # password encryption
    s1 = sha1()
    s1.update(userpwd)
    en_userpwd = s1.hexdigest()

    # ORM
    user = UserInfo()
    user.username = username
    user.userpwd = en_userpwd
    user.useremail = useremail
    user.save()

    return redirect('/user/login/')


# 檢查用戶名是否存在
def register_exist(request):
    username = request.GET.get('username')
    count = UserInfo.objects.filter(username=username).count()
    return JsonResponse({'count': count})


# 用戶登錄
def login(request):
    username = request.COOKIES.get('username', '')

    context = {
        'title': '登錄',
        'error_name': 0,
        'error_pwd': 0,
        'username': username,
    }
    return render(request, 'sf_user/login.html', context)


# 用戶登錄處理
def login_handle(request):
    post = request.POST
    username = post.get('username')
    userpwd = post.get('pwd')
    remb_me = post.get('remb_me', 0)

    user = UserInfo.objects.filter(username=username)

    if len(user) == 1:
        s1 = sha1()
        s1.update(userpwd)
        if s1.hexdigest() == user[0].userpwd:
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)

            # 記住我-選項勾選
            if remb_me == 1:
                red.set_cookie('username', username)
            else:
                red.set_cookie('username', '', max_age=-1)

            # 使用session儲存用戶訊息
            request.session['user_id'] = user[0].id
            request.session['user_name'] = username

            return red

        else:
            context = {
                'title': '登錄',
                'error_name': 0,
                'error_pwd': 1,
                'username': username,
                'userpwd': userpwd,
            }
            return render(request, 'sf_user/login.html', context)

    else:
        context = {
            'title': '登錄',
            'error_name': 1,
            'error_pwd': 0,
            'username': username,
            'userpwd': userpwd,
        }
        return render(request, 'sf_user/login.html', context)


@user_decorator.login
def logout(request):
    request.session.flush()
    return redirect('/')


# 用戶中心-使用者資訊
@user_decorator.login
def info(request):
    user_info = UserInfo.objects.get(id=request.session['user_id'])

    # 最近瀏覽
    goods_list = []
    goods_ids = request.COOKIES.get('goods_ids', '')

    if goods_ids != '':
        goods_ids_list = goods_ids.split(',')
        for goods_id in goods_ids_list:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {
        'title': '用戶中心',
        'user_name': request.session['user_name'],
        'user_phone': user_info.userphone,
        'user_address': user_info.useraddress,
        'page_name': 1,
        'goods_list': goods_list,
    }

    return render(request, 'sf_user/user_center_info.html', context)


# 用戶全部訂單
@user_decorator.login
def order(request, pindex):
    order_list = OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-orderid')
    paginator = Paginator(order_list, 4)

    if pindex == '':
        pindex = '1'

    page = paginator.page(int(pindex))
    context = {
        'title': '用戶中心',
        'page_name': 1,
        'paginator': paginator,
        'page': page,
    }

    return render(request, 'sf_user/user_center_order.html', context)


# 用戶收貨地址
@user_decorator.login
def site(request):
    user_info = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user_info.userreceiver = post.get('receiver')
        user_info.useraddress = post.get('address')
        user_info.userpostalcode = post.get('postalcode')
        user_info.userphone = post.get('phone')
        user_info.save()

    context = {
        'title': '用戶中心',
        'page_name': 1,
        'user_info': user_info,
    }
    return render(request, 'sf_user/user_center_site.html', context)

