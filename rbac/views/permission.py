#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/17 10:50
# @Author  : mark.hu
# @Site    : 
# @File    : permission.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.shortcuts import render, redirect, HttpResponse
from rbac import models
from rbac.forms.permission import PermissionModelForm
from rbac.service.origin_url import memory_reverse_url


def permission_add(request, second_mid):
    """
    添加权限
    :param request:
    :return:
    """

    origin_url = memory_reverse_url(request, "rbac:rbac_menu_list")  # 定义需要返回的地址 前端可以通过此地址跳转
    if request.method == 'GET':  # 请求到页面，生成字段
        form = PermissionModelForm()  # 默认带过来一级菜单
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = PermissionModelForm(data=request.POST)  # 当是POST请求是，表示在增加数据
    if form.is_valid():  # 对数据进行验证
        second_menu_object = models.Permission.objects.filter(id=second_mid).first()  # second_mid二级菜单 检查是否存在二级菜单
        print(second_menu_object)
        if not second_menu_object:  # 不存在返回错误信息
            return HttpResponse("不存在的二级菜单")
        form.instance.pid = second_menu_object  # 在POST提交过来的表单里，添加pid的对象为 二级菜单的对象
        form.save()
        return redirect(origin_url)  # 完成后，跳回到列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def permission_edit(request, pk):
    """
       编辑
       :param request:
       :return:
       """
    origin_url = memory_reverse_url(request, "rbac:rbac_menu_list")
    obj = models.Permission.objects.filter(id=pk).first()  # 数据是否存在
    if not obj:
        return HttpResponse('菜单不存在!')  # 如果不存在，返回错误信息
    if request.method == 'GET':
        form = PermissionModelForm(instance=obj)  # 返回带有数据的页面
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = PermissionModelForm(instance=obj, data=request.POST)  # POST表示修改了 一定要加instance=obj 否则就是增加了
    if form.is_valid():  # 验证信息
        form.save()
        return redirect(origin_url)  # 成功后返回列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def permission_del(request, pk):
    """
    删除
    :param request:
    :return:
    """
    origin_url = memory_reverse_url(request, "rbac:rbac_menu_list")
    if request.method == "GET":
        return render(request, 'rbac/delete.html/', {'pk': pk, "cancel": origin_url})
    models.Permission.objects.filter(id=pk).delete()  # POST请求就删除这条数据
    return redirect(origin_url)  # 跳转回列表页面
