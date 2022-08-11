"""
list :get
create: post
put: update(整体更新，提供所有更改后的字段信息)
patch：partial_update(据不更新，仅提供需要修改的信息)     都要提供id 如 localhost:8080/api/books/2/
delete: destroy
get_id: retrieve
"""
from django.core.mail import send_mail
from rest_framework import viewsets
import hashlib
from apps.models import Users,AdminUsers
from rest_framework.response import Response
from apps.serializers import UserSerializer
from apps.views.ProductInfoViewSet import transFormPages

class Login(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # 跳过权限的登录
    def create(self, request, *args, **kwargs):
        try:
            userName = request.data['userName']
            password = request.data['password']
            try:
                user = Users.objects.get(userName__exact=userName,password__exact=password,is_delete=False)
                print(user.status)
                if user.status:
                    request.session['user'] = user.toDict()  # 添加session
                    return Response({'code': '001', 'user': user.toDict(), 'msg': '登录成功'})
                else:
                    return Response({'code': '004', 'msg': '用户未被激活'})
            except:
                return Response({'code': '004', 'msg': '用户名或密码错误'})
        except:
            return Response({'code': '500','msg': '未知错误'})

class LoginAdmin(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # 跳过权限的登录
    def create(self, request, *args, **kwargs):
        try:
            userName = request.data['userName']
            password = request.data['password']
            try:
                user = AdminUsers.objects.get(userName__exact=userName,password__exact=password,is_delete=False)
                if user.status:
                    request.session['admin'] = user.toDict()  # 添加session
                    return Response({'code': '001', 'user': user.toDict(), 'msg': '登录成功'})
                else:
                    Response({'code': '004', 'msg': '用户已被禁用'})
            except:
                return Response({'code': '004', 'msg': '用户名或密码错误'})
        except:
            return Response({'code': '500','msg': '未知错误'})

class IsRegister(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # 跳过权限的登录
    http_method_names = ['post']  # 允许的请求方法

    def create(self, request, *args, **kwargs):
        try:
            isName = Users.objects.filter(userName__exact=request.data['userName'],status=True,is_delete=False)
            if isName:
                return Response({'code': "004", 'msg': '用户名已经存在，不能注册'})
            else:
                return Response({'code': '001', 'msg': '可以注册'})
        except:
            return Response({'code': '500', 'msg': '未知错误'})

class Register(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # 跳过权限的登录

    # 激活
    def retrieve(self, request, *args, **kwargs):  # 激活用户  改写status为True
        try:
            if request.session['code'] == kwargs['pk']:
                item = Users.objects.get(userName__exact=request.session['userName'])
                item.status = True
                item.save()
                return Response({'code': "001", 'msg': '激活成功!'})
        except:
            return Response({'code': "004", 'msg': '激活失败!'})

    # 注册
    def create(self, request, *args, **kwargs):
        try:
            if Users.objects.filter(userName__exact=request.data['userName']):
                return Response({'code': "004", 'msg': '用户名已经存在，不能注册'})
            else:
                password = request.data['password']
                userInfo = Users(userName=request.data['userName'])
                userInfo.password = password
                userInfo.userPhoneNumber = request.data['userPhoneNumber']  # 用户可以加上userPhoneNumber,乃至地址
                userInfo.userEmail = request.data['userEmail']
                userInfo.save()
                code = hashlib.md5(request.data['userName'].encode(encoding='UTF-8')).hexdigest()
                url = 'http://localhost:8081/#/active?code=' + str(code)
                print(url)
                request.session['code'] = code
                request.session['userName'] = request.data['userName']
                send_mail(
                    '激活邮件',
                    '请点击链接激活账号：' + url,
                    'diningcx@gmail.com',
                    [userInfo.userEmail],
                    fail_silently=False,
                )
                return Response({'code': "001", 'msg': '注册成功,前往邮箱激活'})
        except:
            return Response({'code': '500', 'msg': '未知错误'})

class GetUserInfo(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # 跳过权限的登录

    def list(self, request, *args, **kwargs):
        currentPage = int(request.GET['pagenum'])
        pageSize = int(request.GET['pagesize'])
        query = request.GET['query']
        if query:
            res = Users.objects.filter(userName__contains=query,is_delete=False)
        else:
            res = Users.objects.filter(is_delete=False)
        try:
            totalCount, users = transFormPages(res, currentPage, pageSize)
            return Response({'code': '001', 'users': users, 'total': totalCount})
        except:
            return Response({'code': '002', 'msg': '查询失败'})

#  编辑用户、修改用户状态
class EditUsers(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # 跳过权限的登录

    def create(self, request, *args, **kwargs):
        # 只更新用户的状态
        if request.data['is_change_status'] == 1:
            try:
                user = Users.objects.get(user_id=request.data['user_id'])
                user.status = not user.status
                print(user.status)
                user.save()
                return Response({'code': '001', 'msg': '状态修改成功'})
            except:
                return Response({'code': '002', 'msg': '修改失败'})
        # 更新用户的所有信息
        else:
            try:
                user = Users.objects.get(user_id=request.data['user_id'])
                user.userName = request.data['userName']
                user.userPhoneNumber = request.data['userPhoneNumber']
                user.userEmail = request.data['userEmail']
                user.save()
                return Response({'code': '001', 'msg': '修改成功'})
            except:
                return Response({'code': '002', 'msg': '修改失败'})

class DeleteUser(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # 跳过权限的登录

    def destroy(self, request, *args, **kwargs):
        user_id = int(kwargs['pk'])
        tem = Users.objects.get(user_id__exact=user_id)
        tem.is_delete = True
        tem.save()
        return Response({'code': '001', 'msg': '删除成功'})

class GetMenus(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = []  # 跳过权限的登录

    def list(self, request, *args, **kwargs):
        if request.method == 'GET':
            data = [
                {"authName":'用户管理',"path":'users','id':1,'order':1,'children':[
                    {"authName":'用户列表', "path": 'admin/users', 'id': 1}
                ]},
                {"authName": '订单管理', "path": 'ordersList', 'id': 2, 'order': 2, 'children': [
                    {"authName": '订单列表', "path": 'admin/ordersList', 'id': 1},
                    {"authName": '营收统计', "path": 'admin/ordersIncome', 'id': 2}
                ]},
                {"authName": '商品管理', "path": 'categoryList', 'id': 3, 'order': 3, 'children': [
                    {"authName": '分类列表', "path": 'admin/categoryList', 'id': 1},
                    {"authName": '商品详情', "path": 'admin/productDetails', 'id': 2},
                ]},
                {"authName": '图片管理', "path": 'carouselList', 'id': 4, 'order': 4, 'children': [
                    {"authName": '轮播图管理', "path": 'admin/carouselList', 'id': 1},

                    # 这里改一个按类型查询，默认展示'手机'类型的图片,上面使用面包屑导航
                    {"authName": '商品图片管理', "path": 'admin/productImageList', 'id': 2},
                ]},
            ]
            return Response({'code': '001', 'msg': '查询成功', 'data': data})




