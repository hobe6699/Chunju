#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/17 8:28
# @Author  : mark.hu
# @Site    : 
# @File    : area_class.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.shortcuts import render, redirect, HttpResponse
from webapp.models import msafety
from webapp.forms.area import AreaClassModelForm
from rbac.service.origin_url import memory_reverse_url
from webcore.models.organization import OrgEmp


def area_class_list(request):
    area_class = msafety.AreaClass.objects.all().order_by('id')
    acid = request.GET.get('acid')  # 区域分类ID
    aid = request.GET.get('aid')  # 区域ID
    if acid:
        area = msafety.Area.objects.filter(area_class_id=acid)
    else:
        area = []
    if aid:
        emp = msafety.Area.objects.filter(id=aid).values('emp__name', 'emp__org_dept__name', 'emp__org_position__name',
                                                         'emp__wechat')
    else:
        emp = []
    return render(request,
                  'safety/area_list.html',
                  {"area_class": area_class,
                   'acid': acid,
                   'area': area,
                   'aid': aid,
                   'emp': emp})


def area_class_add(request):
    origin_url = memory_reverse_url(request, "webapp:area_class_list")  # 定义需要返回的地址 前端可以通过此地址跳转
    if request.method == 'GET':  # 请求到页面，生成字段
        form = AreaClassModelForm()
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = AreaClassModelForm(data=request.POST)  # 当是POST请求是，表示在增加数据
    if form.is_valid():  # 对数据进行验证
        form.save()
        return redirect(origin_url)  # 完成后，跳回到列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def area_class_edit(request, pk):
    """
           编辑
           :param request:
           :return:
           """
    origin_url = memory_reverse_url(request, "webapp:area_class_list")
    obj = msafety.AreaClass.objects.filter(id=pk).first()  # 数据是否存在
    if not obj:
        return HttpResponse('菜单不存在!')  # 如果不存在，返回错误信息
    if request.method == 'GET':
        form = AreaClassModelForm(instance=obj)  # 返回带有数据的页面
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = AreaClassModelForm(instance=obj, data=request.POST)  # POST表示修改了 一定要加instance=obj 否则就是增加了
    if form.is_valid():  # 验证信息
        form.save()
        return redirect(origin_url)  # 成功后返回列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def area_class_del(request, pk):
    origin_url = memory_reverse_url(request, "webapp:area_class_list")
    if request.method == "GET":
        return render(request, 'rbac/delete.html/', {'pk': pk, "cancel": origin_url})
    msafety.AreaClass.objects.filter(id=pk).delete()  # POST请求就删除这条数据
    return redirect(origin_url)  # 跳转回列表页面
