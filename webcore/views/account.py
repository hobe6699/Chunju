#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-03 10:14
# @Author  : mark.hu
# @Site    : www.ivan.net.cn
# @File    : login.py
# @Software: PyCharm
from django.shortcuts import render, redirect
from rbac.service.init_permission import init_permission

from webcore.models import organization, system_config
from webcore.utils import md5


def login(request):
    # 1、用户登陆
    if request.method == "GET":
        config_exist = system_config.SystemConfig.objects.count()  # 判断配置信息是否存在
        if config_exist < 1:
            system_config.SystemConfig.objects.create(name='海象软件')  # 不存在就创建
        sys_config = system_config.SystemConfig.objects.all().first()  # 获取配置信息
        return render(request, 'login.html', {'sys_config': sys_config})

    username = request.POST.get('username')
    password = md5.get_md5(request.POST.get('password'))
    print(username, password)

    current_user = organization.OrgEmp.objects.filter(name=username, password=password).first()

    if not current_user:
        return render(request, 'login.html', {'msg': '用户名密码错误.'})
    init_permission(current_user, request)  # 调用权限初始化
    emp = {'pk': current_user.pk,
           'username': current_user.username,
           'name': current_user.name,
           'email': current_user.email,
           'img': str(current_user.img),
           'wechat': current_user.wechat,
           'org_info__name': str(current_user.org_info),
           'org_info__img': str(current_user.org_info.img),
           'org_info__full_name': str(current_user.org_info.full_name),
           'org_info__website': str(current_user.org_info.website),
           'org_dept': str(current_user.org_dept),
           'org_dept__name': str(current_user.org_dept),
           'org_position': str(current_user.org_position.pk),
           'org_position__name': str(current_user.org_position)
           }

    if not emp:
        return render(request, 'login.html', {'msg': '此用户未分配对应的人员信息'})
    request.session['emp'] = emp  # 在session中存人员信息，方便后面调用
    return redirect('/index/')


def logout(request):
    request.session.delete(request.session.session_key)
    return redirect('/login/')


def error(request):
    return render(request, 'error.html',
                  {"error_code": 500, "error_title": "内部服务器错误", "error_content": "内部服务器错误，请尝试重新登陆!",
                   "a_name": "登陆",
                   "a_href": "/login/"})
