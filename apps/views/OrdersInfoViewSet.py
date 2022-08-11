"""
list :get
create: post
put: update(整体更新，提供所有更改后的字段信息)
patch：partial_update(据不更新，仅提供需要修改的信息)     都要提供id 如 localhost:8080/api/books/2/
delete: destroy
get_id: retrieve
"""
import datetime
import json
import time
from django.db import connection
from django.db.migrations import serializer
from django.db.models.functions import TruncMonth
from django.template.defaultfilters import date
from rest_framework import viewsets, status
from apps.models import Orders, Product, ShoppingCart, Category
from django.db.models import Q, Count, Sum
from rest_framework.response import Response
from apps.serializers import OrdersSerializer

# 字典转换
from apps.views.ProductInfoViewSet import transFormPages


def transFormOrders(postId, products):
    data = []
    postId = str(postId)
    for product in products:
        timestamp = str(int(round(time.time() * 1000)))  # 毫秒级时间戳
        order_id = int(postId + timestamp)
        order_time = int(timestamp)
        item_json = {'order_id': order_id, 'product_num': int(product['num']), 'product_price': int(product['price']),
                     'total_price':int(product['price'])*int(product['num']),
                     'user_id': int(postId), 'product_id': int(product['productID']), 'order_time': order_time}
        data.append(item_json)  # 手动填写
    return data


class GetOrder(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = []  # 跳过权限的登录

    def create(self, request, *args, **kwargs):
        postId = str(request.data['user_id'])
        sessionId = str(request.session['user']['user_id'])
        userId = int(sessionId)
        if postId == sessionId:
            orders = Orders.objects.filter(user_id=userId).order_by('-order_time')
            if orders:
                ordersList = []
                for order in orders:
                    o = []
                    product = Product.objects.get(product_id__exact=order.product_id)
                    item_json = {'id': order.id, 'order_id': order.order_id, 'user_id': order.user_id,
                                 'product_id': order.product_id, 'product_num': order.product_num,
                                 'order_time': order.order_time, 'product_price': order.product_price,
                                 'product_name': product.product_name, 'product_picture': product.product_picture, }
                    o.append(item_json)  # 手动填写
                    ordersList.append(o)
                return Response({'code': '001', 'orders': ordersList})
            else:
                return Response({'code': '002', 'msg': '该用户没有订单信息'})
        else:
            return Response({'code': '401', 'msg': '用户名没有登录，请登录后再操作'})


class GetOrderBySearch(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = []  # 跳过权限的登录

    def list(self, request, *args, **kwargs):
        if (request.GET['user_id'] and not request.GET['user_id'].isdigit()) or (request.GET['product_id'] and not request.GET['product_id'].isdigit()):
            return Response({'code': '002', 'msg': 'ID为数字哦!'})

        res = Orders.objects.filter(is_delete=False).order_by('-order_time')
        # 前后端都进行数字校验
        if request.GET['user_id'] and request.GET['user_id'].isdigit():
            res = res.filter(user_id=request.GET['user_id'])
        if request.GET['product_id'] and request.GET['product_id'].isdigit():
            res = res.filter(product_id=request.GET['product_id'])
        if request.GET['startTime'] and request.GET['endTime'] and request.GET['startTime'] <= request.GET['endTime'] and (request.GET['startTime'].isdigit() and request.GET['endTime'].isdigit()):
            res = res.filter(order_time__range=(request.GET['startTime'], request.GET['endTime']))
        if request.GET['order_time'] and request.GET['order_time'].isdigit():
            start_time = int(request.GET['order_time'])  # 由前端完成时间戳转换
            finish_time = start_time + 86400000 - 1000  # 毫秒级时间戳  北京时间加8小时
            res = res.filter(order_time__range=(start_time, finish_time))
        currentPage = request.GET['currentPage']
        pageSize = request.GET['pageSize']
        totalCount, orders = transFormPages(res, currentPage, pageSize)
        return Response({'code': '001', 'Orders': orders, 'total': totalCount, 'msg': '查询成功'})


class AddOrder(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = []  # 跳过权限的登录

    def create(self, request, *args, **kwargs):
        postId = int(request.data['user_id'])
        userId = int(request.session['user']['user_id'])
        products = request.data['products']
        if postId == userId:
            data = transFormOrders(postId, products)
            try:
                for item in data:
                    Orders.objects.create(**item)  # 创建订单、删除购物车原有记录
                    ShoppingCart.objects.filter(user_id=userId, product_id=item['product_id']).delete()
                return Response({'code': '001', 'msg': '购买成功'})
            except:
                return Response({'code': '002', 'msg': '购买失败'})
        else:
            return Response({'code': '401', 'msg': '用户名没有登录，请登录后再操作'})


class DeleteOrder(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = []  # 跳过权限的登录

    def destroy(self, request, *args, **kwargs):
        id = int(kwargs['pk'])
        tem = Orders.objects.get(id__exact=id)
        tem.is_delete = True
        tem.save()
        return Response({'code': '001', 'msg': '删除成功'})


class OrderList(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = []  # 跳过权限的登录

    def list(self, request, *args, **kwargs):
        res = Orders.objects.aggregate(user_num=Count('user_id',distinct=True),product_num=Count('product_id',distinct=True),
                                       order_num=Count('order_id',distinct=True))
        sales = Orders.objects.aggregate(sales=Sum('product_num'),total_price=Sum('total_price'))
        raw_sql = "SELECT FROM_UNIXTIME(order_time/1000,'%Y%m') months,COUNT(id) COUNT FROM orders GROUP BY months"
        with connection.cursor() as cursor:  # with语句用于数据库操作
            cursor.execute(raw_sql)
            dataInfo = cursor.fetchall()

        return Response({'code': '001', 'msg': '数据更新完毕','dataInfo':dataInfo,'res':res,'sales':sales})
