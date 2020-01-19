#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/10 15:11
# @Author  : mark.hu
# @Site    : 
# @File    : index_app.py
# @Software: PyCharm
# @Emial:5898387@qq.com
from django.shortcuts import render, HttpResponse, redirect


def index(request):
    return render(request, 'index_app.html')
