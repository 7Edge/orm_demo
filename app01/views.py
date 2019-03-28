import json
from copy import deepcopy

from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

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


# 专题课程
class CoursesView(APIView):
    pass

    # 创建课程
    def post(self, request):
        serializer_obj = edu_serializers.CourseModelSerializer(data=request.data)
        if serializer_obj.is_valid():
            print(type(serializer_obj.validated_data))
            obj_info = dict(serializer_obj.validated_data)
            many_to_many = obj_info.pop('teacher')
            instance = models.Courses.objects.create(**obj_info)
            instance.teacher.set(many_to_many)  # 创建多对多关系，清空关系再添加关系
            return Response({'code': 1000,
                             'data': serializer_obj.data})
        return Response({'code': 1001,
                         'errors': serializer_obj.errors})


# 专题课程详情
class CourseDetailViewSet(ViewSet):
    queryset = models.Courses.objects.all()
    serializer_class = edu_serializers.PricePolicyModelSerializer

    # @action(detail=True, )

    def price_policies(self, request, pk):
        result = {"code": 1000,
                  "data": None,
                  "error": ""}
        try:
            course_obj = self.queryset.get(pk=pk)
            prices = course_obj.course_pricepolicy_objs.all()
            serializer_obj = self.serializer_class(prices, many=True)
            result['data'] = serializer_obj.data

        except ObjectDoesNotExist:
            result["error"] = "课程不存在！"
            result['code'] = 10001

        return Response(result)

    def add_price_policy(self, request, pk):
        result = {"code": 1000,
                  "data": None,
                  "error": ''}
        try:
            course_obj = self.queryset.get(pk=pk)
            ser_obj = self.serializer_class(data=request.data, many=False)

            if ser_obj.is_valid():
                price_obj = models.PricePolicy.objects.create(course_generic_fk=course_obj, **ser_obj.validated_data)
                result['data'] = self.serializer_class(price_obj).data
            else:
                result['code'] = 10001
                result['error'] = ser_obj.errors
        except ObjectDoesNotExist:
            result["error"] = "课程不存在！"
            result['code'] = 10002

        return Response(result)
