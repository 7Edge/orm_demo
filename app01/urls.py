#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: urls.py
# Date: 3/8/2019
from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import SimpleRouter

from .views import CategoryView, TeacherModelViewSets, CategoryDetailView, CoursesView

router = SimpleRouter()
router.register('teachers', TeacherModelViewSets)

urlpatterns = [
    re_path('categories/$', csrf_exempt(CategoryView.as_view()), name='categories'),
    re_path('categories/(?P<pk>\w+)/$', csrf_exempt(CategoryDetailView.as_view()), name='category-detail'),
    re_path('courses/$', csrf_exempt(CoursesView.as_view()), name='courses'),
]
urlpatterns += router.urls

if __name__ == '__main__':
    pass
