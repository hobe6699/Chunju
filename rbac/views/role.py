#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 13:09
# @Author  : mark.hu
# @Site    : 
# @File    : role.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from rbac import models
from rbac.forms.role import RoleModelForm


def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_queryset = models.Role.objects.all().order_by('id')
    return render(request, 'rbac/role_list.html/', {'roles': role_queryset})


def role_add(request):
    """
    添加角色
    :param request:
    :return:
    """
    origin_url = reverse("rbac:rbac_role_list")  # 定义需要返回的地址 前端可以通过此地址跳转
    if request.method == 'GET':  # 请求到页面，生成字段
        form = RoleModelForm()
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = RoleModelForm(data=request.POST)  # 当是POST请求是，表示在增加数据
    if form.is_valid():  # 对数据进行验证
        form.save()
        return redirect(reverse("rbac:rbac_role_list"))  # 完成后，跳回到列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def role_edit(request, pk):
    """
    编辑角色
    :param request:
    :return:
    """
    origin_url = reverse("rbac:rbac_role_list")  # 定义需要返回的地址 前端可以通过此地址跳转
    obj = models.Role.objects.filter(id=pk).first()  # 数据是否存在
    if not obj:
        return HttpResponse('角色不存在!')  # 如果不存在，返回错误信息
    if request.method == 'GET':
        form = RoleModelForm(instance=obj)  # 返回带有数据的页面
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = RoleModelForm(instance=obj, data=request.POST)  # POST表示修改了 一定要加instance=obj 否则就是增加了
    if form.is_valid():  # 验证信息
        form.save()
        return redirect(reverse("rbac:rbac_role_list"))  # 成功后返回列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def role_del(request, pk):
    """
    删除角色
    :param request:
    :return:
    """
    origin_url = reverse("rbac:rbac_role_list")  # 定义需要返回的地址 前端可以通过此地址跳转
    if request.method == "GET":
        return render(request, 'rbac/delete.html/', {'pk': pk, "cancel": origin_url})
    models.Role.objects.filter(id=pk).delete()  # POST请求就删除这条数据
    return redirect(origin_url)  # 跳转回列表页面
