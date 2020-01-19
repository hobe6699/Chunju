#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-01-03 10:44
# @Author  : mark.hu
# @Site    : www.ivan.net.cn
# @File    : msafety.py
# @Software: PyCharm

from django.db import models
from webcore.models.organization import OrgEmp


class AreaClass(models.Model):
    name = models.CharField(max_length=128, verbose_name='区域分类')
    create_date = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=256, verbose_name="区域名称")
    barcode = models.UUIDField(verbose_name="区域二维码")
    create_date = models.DateTimeField(auto_now=True)
    emp = models.ManyToManyField(OrgEmp, verbose_name="检查人")
    area_class = models.ForeignKey(AreaClass, on_delete=models.CASCADE, verbose_name='区域分类')

    def __str__(self):
        return self.name


class ReviewChecker(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="区域")
    emp = models.ForeignKey(OrgEmp, on_delete=models.CASCADE, verbose_name='复查人')
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.area, self.emp


class CheckRecord(models.Model):
    emp = models.ForeignKey(OrgEmp, on_delete=models.CASCADE, verbose_name='检查人')
    create_date = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    area = models.ForeignKey(to="Area", on_delete=models.CASCADE, verbose_name="区域名称")
    state = models.BooleanField(default=True, verbose_name="状态")
    description = models.CharField(max_length=256, verbose_name="说明", null=True)


class CheckImage(models.Model):
    check_record = models.ForeignKey("CheckRecord", on_delete=models.CASCADE)
    img = models.ImageField(upload_to='media', verbose_name="检查图片")
    shooting_time = models.DateTimeField(verbose_name="拍摄时间", null=True, auto_now=True)
