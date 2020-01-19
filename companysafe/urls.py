#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 15:11
# @Author  : mark.hu
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @Emial:5898387@qq.com
from django.urls import path, re_path
from companysafe.views import *

app_name = 'companysafe'
urlpatterns = [
    re_path(r"^inspection_record/$", inspection.inspection_record),

]
