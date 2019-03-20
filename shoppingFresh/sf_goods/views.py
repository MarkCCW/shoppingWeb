# coding:utf-8
from django.shortcuts import render
from models import TypeInfo, GoodsInfo
from django.core.paginator import Paginator
from sf_cart.models import CartInfo


def index(request):
    # 查詢各類別中最新4條數據/最熱門4條數據
    typelist = TypeInfo.objects.all()

    type_newest_0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type_hottest_0 = typelist[0].goodsinfo_set.order_by('-goodsclick')[0:4]
    type_newest_1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type_hottest_1 = typelist[1].goodsinfo_set.order_by('-goodsclick')[0:4]
    type_newest_2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type_hottest_2 = typelist[2].goodsinfo_set.order_by('-goodsclick')[0:4]
    type_newest_3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type_hottest_3 = typelist[3].goodsinfo_set.order_by('-goodsclick')[0:4]
    type_newest_4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type_hottest_4 = typelist[4].goodsinfo_set.order_by('-goodsclick')[0:4]
    type_newest_5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type_hottest_5 = typelist[5].goodsinfo_set.order_by('-goodsclick')[0:4]

    context = {
        'title': '首頁', 'guest_cart': 1,
        'type_newest_0': type_newest_0, 'type_hottest_0': type_hottest_0,
        'type_newest_1': type_newest_1, 'type_hottest_1': type_hottest_1,
        'type_newest_2': type_newest_2, 'type_hottest_2': type_hottest_2,
        'type_newest_3': type_newest_3, 'type_hottest_3': type_hottest_3,
        'type_newest_4': type_newest_4, 'type_hottest_4': type_hottest_4,
        'type_newest_5': type_newest_5, 'type_hottest_5': type_hottest_5,
        'cart_count': cart_count(request)
        }
    return render(request, 'sf_goods/index.html', context)


# 商品列表頁
def list(request, typeid, pindex, sort):
    """
    :param typeid: 商品分類號碼
    :param pindex: 分頁編號
    :param sort: 分頁排序依據
    """

    typeinfo = TypeInfo.objects.get(pk=int(typeid))
    newest = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    # order by newest
    if sort == '1':
        goods_list = GoodsInfo.objects.filter(goodstype_id=int(typeid)).order_by('-id')
    # order by price
    elif sort == '2':
        goods_list = GoodsInfo.objects.filter(goodstype_id=int(typeid)).order_by('-goodsprice')
    # order by click
    elif sort == '3':
        goods_list = GoodsInfo.objects.filter(goodstype_id=int(typeid)).order_by('-goodsclick')

    paginator = Paginator(goods_list, 5)
    page = paginator.page(int(pindex))
    context = {
        'guest_cart': 1,
        'title': typeinfo.typetitle,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,
        'newest': newest,
        'cart_count': cart_count(request),
    }

    return render(request, 'sf_goods/list.html', context)


# 商品詳情內容
def detail(request, id):
    goods_info = GoodsInfo.objects.get(pk=int(id))
    goods_info.goodsclick += 1
    goods_info.save()

    newest = goods_info.goodstype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'guest_cart': 1,
        'title': goods_info.goodstype.typetitle,
        'goods':goods_info,
        'newest': newest,
        'id': id,
        'cart_count': cart_count(request),
    }
    response = render(request, 'sf_goods/detail.html', context)

    # 紀錄最近瀏覽,在用戶中心顯示
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = '%d'%goods_info.id

    # 判斷是否有瀏覽紀錄
    if goods_ids != '':
        goods_ids_list = goods_ids.split(',')

        # 刪除重複商品瀏覽記錄
        if goods_ids_list.count(goods_id) >= 1:
            goods_ids_list.remove(goods_id)
        goods_ids_list.insert(0, goods_id)

        # 超過六個商品紀錄,則刪除一個最舊紀錄
        if len(goods_ids_list) >= 6:
            del goods_ids_list[5]
        goods_ids = ','.join(goods_ids_list)

    else:
        # 如無瀏覽紀錄則直接添加
        goods_ids = goods_id

    response.set_cookie('goods_ids', goods_ids)
    return response


# 購物車數量
def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0


# 商品搜索查詢
from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title'] = '搜尋商品'
        context['guest_cart'] = 1
        context['cart_count'] = cart_count(self.request)
        return context
