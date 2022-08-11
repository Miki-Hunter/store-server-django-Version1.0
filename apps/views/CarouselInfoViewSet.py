"""
list :get
create: post
put: update(整体更新，提供所有更改后的字段信息)
patch：partial_update(据不更新，仅提供需要修改的信息)     都要提供id 如 localhost:8080/api/books/2/
delete: destroy
get_id: retrieve
"""
import os
import time
from os.path import splitext

from rest_framework import viewsets, status
from rest_framework.response import Response
from xiaomiStore.settings import PROJECT_ROOT
from apps.models import Carousel
from apps.serializers import CarouselSerializer


class CarouselInfo(viewsets.ModelViewSet):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer
    permission_classes = []  # 跳过权限的登录

    def list(self, request, *args, **kwargs):
        alist = Carousel.objects.filter()
        carousel = []
        for _ in alist:
            item = {'carousel_id': _.carousel_id, 'imgPath': _.imgPath}
            carousel.append(item)
        return Response({"code": '001', 'carousel': carousel})

    def destroy(self, request, *args, **kwargs):
        carousel_id = kwargs['pk']
        try:
            tem = Carousel.objects.get(carousel_id__exact=int(carousel_id))
            path = tem.imgPath
            os.remove(PROJECT_ROOT + '\\' + path)
            tem.delete()
            return Response({"code": '001', 'msg': '删除成功'})
        except:
            return Response({"code": '002', 'msg': '图片不存在或已损坏'})

    def create(self, request, *args, **kwargs):
        try:
            pic = request.FILES['file']
            pic_type = os.path.splitext(pic.name)[-1]
            sqlPath = 'public\\imgs\\carousel\\' + 'Carousel' + str(round(time.time()) % 10000) + pic_type
            # 为了避免有人把图片名称弄得很长，影响数据库的写入，不使用自带名称
            # sqlPath = 'public\\imgs\\carousel\\' + str(time.time() // 10000) + pic.name
            save_path = PROJECT_ROOT + '\\' + sqlPath
            with open(save_path, "wb") as f:
                for content in pic.chunks():
                    f.write(content)
            f.close()
            Carousel.objects.create(imgPath=sqlPath)
            return Response({"code": '001', 'msg': '上传成功!'})
        except:
            return Response({"code": '002', 'msg': '上传失败!'})



