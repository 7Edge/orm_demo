import json

from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from .models import Category
from app01 import models

from app01.serializers import edu_serializers


# Create your views here.

# 分类操作
class CategoryView(View):
    def post(self, request, *args, **kwargs):
        valid_data = request.POST.dict()  # 这样拿到全部参数，同key只取最后一个值
        try:
            Category.objects.create(**valid_data)  # 创建数据
        except Exception as e:
            return HttpResponse('创建失败')
        return HttpResponse('创建成功！')

    def get(self, request, *args, **kwargs):
        qs = Category.objects.all()
        content = dict()
        for item in qs:
            content[item.pk] = item.title
            print(item.title, type(item.title))
        return JsonResponse(content)


class CategoryDetailView(APIView):
    def put(self, request, pk):
        try:
            obj = Category.objects.get(pk=pk)
            for k, v in request.data.dict().items():
                setattr(obj, k, v)
            obj.save()
            print(request.data.dict())
        except ObjectDoesNotExist as e:
            print(e)
            return HttpResponse('目标对象不存在！')
        return HttpResponse('更新成功！')


# 老师视图
class TeacherModelViewSets(ModelViewSet):
    queryset = models.Teachers.objects.all()
    serializer_class = edu_serializers.TeacherModelSerializer
