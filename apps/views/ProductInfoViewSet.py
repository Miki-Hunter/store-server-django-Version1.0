import os
import time

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from rest_framework import viewsets
from apps.models import Product,Category,ProductPicture
from rest_framework.response import Response
from apps.serializers import ProductSerializer

# 将对象转换为字典
from xiaomiStore.settings import PROJECT_ROOT


def transFormProduct(goods_list):
    json_list = []
    for goods in goods_list:
        json_item = model_to_dict(goods) # 将对象转换为字典
        json_list.append(json_item)
    return json_list

# 页码转换
def transFormPages(res,currentPage,pageSize):
    paginator = Paginator(res, pageSize)  # 生成分页实例
    totalCount = paginator.count  # 获取数据总条数
    try:
        page_res = paginator.page(currentPage)
    except PageNotAnInteger:
        page_res = paginator.page(1)
    except EmptyPage:
        page_res = paginator.page(1)
    finalList = []
    for _ in page_res:
        finalList.append(model_to_dict(_))
    return totalCount,finalList

class GetPromoProduct(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # 跳过权限的登录

    def create(self, request, *args, **kwargs):
        categoryName = str(request.data['categoryName'])
        category_id = Category.objects.get(category_name=categoryName).category_id
        product_7 = Product.objects.filter(category_id=category_id).order_by('product_sales')[:7]
        finalProduct_7 = transFormProduct(product_7)
        return Response({'code': '001', 'Product': finalProduct_7})

class GetDetails(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # 跳过权限的登录

    def create(self, request, *args, **kwargs):
        productSearch = str(request.data['productSearch'])
        if productSearch.isdigit():
            product = Product.objects.filter(product_id=int(productSearch))
        else:
            product = Product.objects.filter(product_name__contains=productSearch)
        productDetails = transFormProduct(product)
        if productDetails:
            return Response({'code': '001', 'Product': productDetails})
        else:
            return Response({'code': '002', 'msg': '没有这个商品或已经被删除'})

class GetCategory(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # 跳过权限的登录

    def list(self, request, *args, **kwargs):
        categorys = Category.objects.filter()
        category_list = []
        for item in categorys:
            json_item = {'category_id':item.category_id,'category_name':item.category_name}
            category_list.append(json_item)
        return Response({'code': '001', 'category': category_list})

class GetAllProduct(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # 跳过权限的登录

    def create(self, request, *args, **kwargs):
        currentPage = int(request.data['currentPage'])
        pageSize = int(request.data['pageSize'])
        try:
            res = Product.objects.all().order_by('-product_sales')
            totalCount,products =transFormPages(res, currentPage, pageSize)
            return Response({'code': '001', 'Product': products, 'total': totalCount})
        except:
            return Response({'code': '002', 'msg': '查询失败'})

class GetHotProduct(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # 跳过权限的登录

    def create(self, request, *args, **kwargs):
        try:
            categoryNames = request.data['categoryName']
            category_ids = []
            for categoryName in categoryNames:
                category_id = Category.objects.get(category_name=categoryName).category_id
                category_ids.append(category_id)
            raw_sql = 'select * from Product where category_id = ' + str(category_ids[0])
            for i in (1,len(category_ids)-1):
                raw_sql += ' or category_id = ' + str(category_ids[i])
            raw_sql += ' order by product_sales desc limit 0 , 7 '
            product_7 = Product.objects.raw(raw_sql)  # 查询多种类别的热销商品, 这里直接用了原生sql语句搜索了前7条数据
            product_7 = transFormProduct(product_7)
            return Response({'code': '001', 'Product': product_7})
        except:
            return Response({'code': '002', 'msg': '查询失败'})

class GetProductByCategory(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # 跳过权限的登录

    def create(self, request, *args, **kwargs):
        try:
            categoryID = request.data['categoryID']
            currentPage = request.data['currentPage']
            pageSize = request.data['pageSize']
            # 这里的categoryID是一个数组，所以要用下标查询
            res = Product.objects.filter(category_id=categoryID[0]).order_by('product_sales')
            # 按照销量排序
            totalCount,products = transFormPages(res, currentPage, pageSize)
            return Response({'code': '001', 'Product': products, 'total': totalCount})
        except:
            return Response({'code': '002', 'msg': '查询失败'})

class GetProductBySearch(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # 跳过权限的登录

    def create(self, request, *args, **kwargs):
        search = request.data['search']
        currentPage = request.data['currentPage']
        pageSize = request.data['pageSize']
        categoryNames = Category.objects.filter(category_name__exact=search)
        # 是否有该类别
        if categoryNames:
            categoryID = categoryNames[0].category_id
            res = Product.objects.filter(category_id=categoryID).order_by('-product_sales')
            totalCount,products = transFormPages(res, currentPage, pageSize)
            return Response({'code': '001', 'Product': products, 'total': totalCount})
        # 没有该类别，按照商品名模糊搜索
        else:
            res = Product.objects.filter(product_name__contains=search).order_by('-product_sales')
            totalCount,products = transFormPages(res, currentPage, pageSize)
            return Response({'code': '001', 'Product': products, 'total': totalCount})

class DeleteProduct(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # 跳过权限的登录

    def destroy(self, request, *args, **kwargs):
        product_id = kwargs['pk']
        try:
            tem = Product.objects.get(product_id=product_id)
            tem.is_delete = True
            tem.save()
            return Response({'code': '001', 'msg': '删除成功'})
        except:
            return Response({'code': '002', 'msg': '删除失败'})

class UpdateProduct(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # 跳过权限的登录

    def create(self, request, *args, **kwargs):
        product_update = request.data
        try:
            Product.objects.filter(product_id=product_update['product_id']).update(**product_update)
            return Response({'code': '001', 'msg': '修改成功'})
        except:
            return Response({'code': '002', 'msg': '修改失败'})

class GetDetailsPicture(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # 跳过权限的登录

    # 获取
    def list(self, request, *args, **kwargs):
        try:
            product_id = request.GET['productID']
            productPicture = ProductPicture.objects.filter(product_id=int(product_id))
            finalPictures = transFormProduct(productPicture)
            return Response({'code': '001', 'ProductPicture': finalPictures,'msg':'获取成功'})
        except:
            return Response({'code': '002', 'msg':'找不到商品图片'})
    # 删除
    def destroy(self, request, *args, **kwargs):
        try:
            imag_id = kwargs['pk']
            tem = ProductPicture.objects.get(id__exact=int(imag_id))
            path = tem.product_picture
            os.remove(PROJECT_ROOT + '\\' + path)
            tem.delete()
            return Response({"code": '001', 'msg': '删除成功'})
        except:
            return Response({"code": '002', 'msg': '图片不存在或已损坏'})
    # 添加
    def create(self, request, *args, **kwargs):
        try:
            pic = request.FILES['file']
            product_id = request.data['productID']
            print(product_id)
            pic_type = os.path.splitext(pic.name)[-1]
            sqlPath = 'public\\imgs\\phone\\picture\\' + 'product' + str(round(time.time()) % 10000) + pic_type
            save_path = PROJECT_ROOT + '\\' + sqlPath
            with open(save_path, "wb") as f:
                for content in pic.chunks():
                    f.write(content)
            f.close()
            ProductPicture.objects.create(product_picture=sqlPath,product_id=product_id)
            return Response({"code": '001', 'msg': '上传成功!'})
        except:
            return Response({"code": '002', 'msg': '上传失败!'})