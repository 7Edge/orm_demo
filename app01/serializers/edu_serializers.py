#!/usr/bin/env python
# coding=UTF-8
# author: zhangjiaqi <1399622866@qq.com>
# File: edu_serializers.py
# Date: 3/11/2019
from rest_framework import serializers

from app01 import models


# 老师序列化
class TeacherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teachers
        fields = '__all__'


if __name__ == '__main__':
    pass
