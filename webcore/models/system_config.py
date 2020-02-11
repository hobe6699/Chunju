#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/11 13:23
# @Author  : mark.hu
# @Site    : 
# @File    : system.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.db import models


class SystemConfig(models.Model):
    name = models.CharField(verbose_name='系统名称', max_length=512)
    ico = models.ImageField(upload_to='sys', verbose_name='系统图标', default='sys/logo.png')
    background_img = models.ImageField(upload_to='sys', verbose_name='登陆页背景图片', default='sys/bg1.jpg')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sys_config'
        app_label = 'webcore'
