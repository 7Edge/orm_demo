from django.test import TestCase

# Create your tests here.


from django.db.models import Model

from django.forms import ModelForm

from django.http import JsonResponse

from rest_framework import generics

from rest_framework import serializers

from rest_framework.relations import PrimaryKeyRelatedField

from rest_framework import viewsets

from rest_framework import routers

from django.contrib.contenttypes import fields

from django.db.models import ForeignKey
from django.db.models import ManyToManyField
