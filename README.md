# ShoppingFresh
使用Django開發購物網站DEMO


<生鮮購物網站首頁>

![index][https://github.com/MarkCCW/shoppingWeb/blob/master/readme_pic/index.png]

<用戶登入>

![login][https://github.com/MarkCCW/shoppingWeb/blob/master/readme_pic/login.png]

<用戶註冊>

![register][https://github.com/MarkCCW/shoppingWeb/blob/master/readme_pic/register.png]

<購物車內容>

![cart][https://github.com/MarkCCW/shoppingWeb/blob/master/readme_pic/cart.png]

<訂單資訊>

![orders][https://github.com/MarkCCW/shoppingWeb/blob/master/readme_pic/order.png]

<搜尋商品>

![search][https://github.com/MarkCCW/shoppingWeb/blob/master/readme_pic/search.png]

## 主要功能介紹
- 1.使用者相關資訊
- 2.商品類別及詳細資訊
- 3.購物車內容資訊 
- 4.訂單內容及購買流程
- 5.搜尋商品

## Django-MTV架構
### Model
使用Django封裝好的ORM，對資料庫做數據的相關操作，數據分成以下部分：
- 使用者：UserInfo
- 商品：TypeInfo, GoodsInfo
- 購物車：CartInfo
- 訂單：OrderInfo, OrderDetailInfo
```python
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
```
### Template
將模板內容重複的部分使用繼承方式來編寫，`base.html`呈現網頁頂部的選項，`base_bottom.html`呈現網頁底部的資訊
```html
{% extends "base_bottom.html" %}
{% block head %}...{% endblock head %}
{% block body %}
	<div class="login_top clearfix">
		<a href="/" class="login_logo"><img src="/static/images/logo02.png"></a>
	</div>
	<div class="login_form_bg">
		<div class="login_form_wrap clearfix">
			<div class="login_banner fl"></div>
			<div class="slogan fl">生鮮購物 · 快速送達</div>
			<div class="login_form fr">
				<div class="login_title clearfix">
					<h1>用户登錄</h1>
					<a href="/user/register/">立即註冊</a>
				</div>
				<div class="form_input">
					<form action="/user/login_handle/" method="post">
						{% csrf_token %}
						<input type="text" name="username" class="name_input" value="{{username}}" placeholder="請輸入用户名">
						<div class="user_error">輸入錯誤</div>
						<input type="password" name="pwd" class="pass_input" value="{{userpwd}}" placeholder="請輸入密碼">
						<div class="pwd_error">輸入錯誤</div>
						<div class="more_input clearfix">
							<input type="checkbox" name="remb_me" value="1" checked="checked">
							<label>記住用户名</label>
							<a href="#">忘記密碼</a>
						</div>
						<input type="submit" name="" value="登錄" class="input_submit">
					</form>
				</div>
			</div>
		</div>
	</div>
{% endblock body %}
```
### View
Django的MTV架構`(Model-Template-View)`，一般MVC架構的View是用來呈現獲取的資料給使用者，而Django的View的目的不是"資料如何呈現"，而是"呈現哪一個資料"。
```python
def login(request):
    username = request.COOKIES.get('username', '')
    context = {
        'title': '登錄',
        'error_name': 0,
        'error_pwd': 0,
        'username': username,
    }
    return render(request, 'sf_user/login.html', context)
```

## 其他實作功能介紹
### 用戶登入驗證-裝飾器
登入驗證：透過url請求用戶相關資訊時，都先檢查用戶是否在登入狀態下進行請求
驗證方式：用戶驗證模組python裝飾器`user_decorator.py`:
```python
def login(func):
    def login_func(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url', request.get_full_path())
            return red

    return login_func
```
在登入驗證的功能前面加上`@user_decorator.login`:
```python
@user_decorator.login
def info(request):
    user_info = UserInfo.objects.get(id=request.session['user_id'])
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
```

### 用戶提交訂單-資料庫的事務功能
```python
@transaction.atomic
@user_decorator.login
def order_handle(request):
    # 創建回歸點
    point = transaction.savepoint()
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
            cart = CartInfo.objects.get(id=id1)
            goods = cart.goods
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
        # 捕捉異常,操作失敗
        print '================%s'%e
        transaction.savepoint_rollback(point)
    
    return redirect('/user/order/')
```
### 商品搜尋功能
使用`haystack`模組並搭配`whoosh`搜尋引擎
```python
from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title'] = '搜尋商品'
        context['guest_cart'] = 1
        context['cart_count'] = cart_count(self.request)
        return context
```
