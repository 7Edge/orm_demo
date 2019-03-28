from django.contrib import admin

# Register your models here.

from app01 import models


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__']


admin.site.register(models.Courses, CourseAdmin)
admin.site.register(models.Category)
admin.site.register(models.Teachers)
admin.site.register(models.PricePolicy)
admin.site.register(models.DegreeCourses)
admin.site.register(models.ContentType)
