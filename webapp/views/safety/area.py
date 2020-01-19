#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/17 8:28
# @Author  : mark.hu
# @Site    : 
# @File    : area_class.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.shortcuts import render, redirect, HttpResponse
from rbac.service.origin_url import memory_reverse_url
from webapp.forms.area import AreaModelForm
from webapp.models import msafety
import uuid


def area_list(request):
    return render(request, 'safety/area_list.html')


def area_add(request, acid):
    area_class_object = msafety.AreaClass.objects.filter(id=acid).first()
    origin_url = memory_reverse_url(request, "webapp:area_class_list")  # 定义需要返回的地址 前端可以通过此地址跳转
    if request.method == 'GET':  # 请求到页面，生成字段
        form = AreaModelForm(initial={'area_class': area_class_object, 'barcode': uuid.uuid1()})
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = AreaModelForm(data=request.POST)  # 当是POST请求是，表示在增加数据
    if form.is_valid():  # 对数据进行验证
        form.save()
        return redirect(origin_url)  # 完成后，跳回到列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def area_edit(request, pk):
    origin_url = memory_reverse_url(request, "webapp:area_class_list")
    obj = msafety.Area.objects.filter(id=pk).first()  # 数据是否存在
    if not obj:
        return HttpResponse('菜单不存在!')  # 如果不存在，返回错误信息
    if request.method == 'GET':
        form = AreaModelForm(instance=obj)  # 返回带有数据的页面
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = AreaModelForm(instance=obj, data=request.POST)  # POST表示修改了 一定要加instance=obj 否则就是增加了
    if form.is_valid():  # 验证信息
        form.save()
        return redirect(origin_url)  # 成功后返回列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def area_del(request, pk):
    """
        删除
        :param request:
        :return:
        """
    origin_url = memory_reverse_url(request, "webapp:area_class_list")
    if request.method == "GET":
        return render(request, 'rbac/delete.html/', {'pk': pk, "cancel": origin_url})
    msafety.Area.objects.filter(id=pk).delete()  # POST请求就删除这条数据
    return redirect(origin_url)  # 跳转回列表页面
