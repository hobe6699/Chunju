#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 15:14
# @Author  : mark.hu
# @Site    : 
# @File    : imspection.py
# @Software: PyCharm
# @Emial:5898387@qq.com
from django.shortcuts import render


def inspection_record(request):
    return render(request, 'inspection_record.html')
