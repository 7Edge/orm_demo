from django.db import models
from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType


# Create your models here.

# 老师表
class Teachers(models.Model):
    name = models.CharField(verbose_name='老师名', max_length=64)
    age = models.PositiveSmallIntegerField(verbose_name='年龄')

    class Meta:
        verbose_name_plural = '001. 老师表'

    def __str__(self):
        return self.name


# 课程分类
class Category(models.Model):
    title = models.CharField(verbose_name='类名', max_length=32)

    class Meta:
        verbose_name_plural = '002. 课程分类'

    def __str__(self):
        return self.title


# 专题课
class Courses(models.Model):
    title = models.CharField(verbose_name='课程名', max_length=32)
    level_choices = (
        (0, '入门'),
        (1, '中级'),
        (2, '高级')
    )
    level = models.PositiveSmallIntegerField(verbose_name='难度等级', choices=level_choices, default=1, help_text='默认中级')
    teacher = models.ManyToManyField(verbose_name='任课老师s', to='Teachers')
    category = models.ForeignKey(verbose_name='所属课程类', to='Category', to_field='id', on_delete=models.CASCADE)

    # GenericRelated 价格策略
    course_pricepolicy_objs = fields.GenericRelation(to='PricePolicy', object_id_field='object_id',
                                                     content_type_field='content_type')

    class Meta:
        verbose_name_plural = '003. 专题课'

    def __str__(self):
        return self.title


# 学位课
class DegreeCourses(models.Model):
    title = models.CharField(verbose_name='学位课', max_length=32)
    level_choices = (
        (0, '入门'),
        (1, '中级'),
        (2, '高级')
    )
    level = models.PositiveSmallIntegerField(verbose_name='难度等级', choices=level_choices, default=1, help_text='默认中级')
    teacher = models.ManyToManyField(verbose_name='任课老师s', to='Teachers')
    category = models.ForeignKey(verbose_name='所属课程类', to='Category', to_field='id', on_delete=models.CASCADE)

    degreecourse_pricepolicy_qs = fields.GenericRelation(to='PricePolicy', object_id_field='object_id',
                                                         content_type_field='content_type')

    class Meta:
        verbose_name_plural = '004. 学位课'

    def __str__(self):
        return self.title


# 价格策略表
class PricePolicy(models.Model):
    during_choices = (
        (1, '一天'),
        (7, '一周'),
        (14, '两周'),
        (30, '一个月'),
        (180, '半年'),
        (365, '一年'),
        (730, '两年'),
    )
    during = models.PositiveIntegerField(verbose_name='学习周期', choices=during_choices)
    price = models.DecimalField(verbose_name='价格', max_digits=8, decimal_places=2, help_text='精确到小数点后两位')

    object_id = models.IntegerField(verbose_name='generic_fk_course')
    content_type = models.ForeignKey(verbose_name='表ID', to=ContentType, on_delete=models.CASCADE)

    # content_obj
    course_generic_fk = fields.GenericForeignKey()

    class Meta:
        unique_together = ('object_id', 'content_type', 'price')
        verbose_name_plural = '005. 课程价格策略表'

    def __str__(self):
        return self.course_generic_fk.title + '-' + self.get_during_display() + str(self.price)
