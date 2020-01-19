#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-03 10:14
# @Author  : mark.hu
# @Site    : www.ivan.net.cn
# @File    : login.py
# @Software: PyCharm
from django.shortcuts import render, HttpResponse, redirect
from rbac.service.init_permission import init_permission
from rbac.models import UserInfo
from webcore.models import organization


def login(request):
    # 1、用户登陆
    if request.method == "GET":
        org = organization.OrgInfo.objects.all().first()  # 获取公司配置信息
        return render(request, 'login.html', {"org": org})
    username = request.POST.get('username')
    password = request.POST.get('password')
    current_user = UserInfo.objects.filter(name=username, password=password).first()
    # print(current_user)
    if not current_user:
        return render(request, 'login.html', {'msg': '用户名密码错误.'})
    init_permission(current_user, request)  # 调用权限初始化
    emp = organization.OrgEmp.objects.filter(account=current_user).values('pk', 'name', 'org_info', 'org_info__name',
                                                                          'org_info__img', 'org_info__full_name',
                                                                          'org_info__website',
                                                                          'org_dept', 'org_dept__name', 'org_position',
                                                                          'org_position__name', 'account',
                                                                          'account__name', 'account__email', 'img',
                                                                          'wechat').first()  # 获取人员信息
    if not emp:
        return render(request, 'login.html', {'msg': '此用户未分配对应的人员信息'})
    request.session['emp'] = emp  # 在session中存人员信息，方便后面调用
    return redirect('/webcore/index/')


def logout(request):
    request.session.delete(request.session.session_key)
    return redirect('/webcore/login/')


def error(request):
    return render(request, 'error.html',
                  {"error_code": 500, "error_title": "内部服务器错误", "error_content": "内部服务器错误，请尝试重新登陆!",
                   "a_name": "登陆",
                   "a_href": "/webcore/login/"})
