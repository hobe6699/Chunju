#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-03 10:14
# @Author  : mark.hu
# @Site    : www.ivan.net.cn
# @File    : login.py
# @Software: PyCharm
from django.db import models
from django.shortcuts import render, HttpResponse, redirect
from rbac.service.init_permission import init_permission
from rbac import models


def login(request):
    # 1、用户登陆
    if request.method == "GET":
        return render(request, 'login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    print(user)
    current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名密码错误.'})

    init_permission(current_user, request)  # 调用权限初始化

    return redirect('/web/customer/list/')
