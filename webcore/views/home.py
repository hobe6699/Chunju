#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 8:59
# @Author  : mark.hu
# @Site    : 
# @File    : index.py
# @Software: PyCharm
# @Emial:5898387@qq.com
from django.shortcuts import render, HttpResponse, redirect


def layout(request):
    return render(request, 'layout.html')


def index(request):
    emp = request.session.get('emp')
    print(emp)
    if not emp:
        return redirect('/')
    return render(request, 'index.html', {"emp": emp})


def index_v1(request):
    return render(request, 'index_v1.html')


def success(request):
    msg = request.session['msg']
    return render(request, 'public/success.html',{'msg':msg})
