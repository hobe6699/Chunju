#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/16 14:28
# @Author  : mark.hu
# @Site    : 
# @File    : menu.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.shortcuts import render, redirect, HttpResponse
from rbac import models
from django.urls import reverse
from django.forms import formset_factory
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, MultiAddPermissionForm, MultiEditPermissionForm
from rbac.service.origin_url import memory_reverse_url
from rbac.service.routes import *


def menu_list(request):
    menus = models.Menu.objects.all().order_by('sort')
    mid = request.GET.get('mid')  # 一级菜单ID
    second_mid = request.GET.get('second_mid')  # 二级菜单ID
    if mid:
        second_menus = models.Permission.objects.filter(menu_id=mid).all().order_by('sort')
    else:
        second_menus = []
    if second_mid:
        permission = models.Permission.objects.filter(pid=second_mid).all().order_by('sort')
    else:
        permission = []
    return render(request, 'rbac/menu_list.html',
                  {"menus": menus,
                   "menu_id": mid,
                   'second_mid': second_mid,
                   'second_menus': second_menus,
                   'permission': permission})


def menu_add(request):
    """
    添加菜单
    :param request:
    :return:
    """
    origin_url = memory_reverse_url(request, "rbac:rbac_menu_list")  # 定义需要返回的地址 前端可以通过此地址跳转
    if request.method == 'GET':  # 请求到页面，生成字段
        form = MenuModelForm()
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = MenuModelForm(data=request.POST)  # 当是POST请求是，表示在增加数据
    if form.is_valid():  # 对数据进行验证
        form.save()
        return redirect(origin_url)  # 完成后，跳回到列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def menu_edit(request, pk):
    """
       编辑
       :param request:
       :return:
       """
    origin_url = memory_reverse_url(request, "rbac:rbac_menu_list")
    obj = models.Menu.objects.filter(id=pk).first()  # 数据是否存在
    if not obj:
        return HttpResponse('菜单不存在!')  # 如果不存在，返回错误信息
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)  # 返回带有数据的页面
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = MenuModelForm(instance=obj, data=request.POST)  # POST表示修改了 一定要加instance=obj 否则就是增加了
    if form.is_valid():  # 验证信息
        form.save()
        return redirect(origin_url)  # 成功后返回列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def menu_del(request, pk):
    """
        删除角色
        :param request:
        :return:
        """
    origin_url = memory_reverse_url(request, "rbac:rbac_menu_list")
    if request.method == "GET":
        return render(request, 'rbac/delete.html/', {'pk': pk, "cancel": origin_url})
    models.Menu.objects.filter(id=pk).delete()  # POST请求就删除这条数据
    return redirect(origin_url)  # 跳转回列表页面


def second_add(request, menu_id):
    """
    添加权限
    :param request:
    :return:
    """
    menu_object = models.Menu.objects.filter(id=menu_id).first()  # menu_id默认带过来的一级菜单
    origin_url = memory_reverse_url(request, "rbac:rbac_menu_list")  # 定义需要返回的地址 前端可以通过此地址跳转
    if request.method == 'GET':  # 请求到页面，生成字段
        form = SecondMenuModelForm(initial={'menu': menu_object})  # 默认带过来一级菜单 设置默认值
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = SecondMenuModelForm(data=request.POST)  # 当是POST请求是，表示在增加数据
    if form.is_valid():  # 对数据进行验证
        form.save()
        return redirect(origin_url)  # 完成后，跳回到列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def second_edit(request, pk):
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
        form = SecondMenuModelForm(instance=obj)  # 返回带有数据的页面
        return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})
    form = SecondMenuModelForm(instance=obj, data=request.POST)  # POST表示修改了 一定要加instance=obj 否则就是增加了
    if form.is_valid():  # 验证信息
        form.save()
        return redirect(origin_url)  # 成功后返回列表页面
    return render(request, 'rbac/change.html/', {'form': form, "cancel": origin_url})  # 否则返回错误信息


def second_del(request, pk):
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


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')
    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0, )  # extra 是否可以额外添加
    generate_formset = None
    if request.method == 'POST' and post_type == 'generate':  # 批量添加
        formset = generate_formset_class(data=request.POST)  # 获取提交过来的数据
        if formset.is_valid():  # 进行验证
            object_list = []
            post_row_list = formset.cleaned_data  # 将数据存一份出来
            has_error = False  # 是否出错
            for i in range(0, formset.total_form_count()):  # 循环验证每一行数据，是否在数据库中存在
                row_dict = post_row_list[i]
                print(row_dict)
                row_dict.pop('pid')
                print(row_dict)
                try:
                    new_object = models.Permission(**row_dict)
                    new_object.validate_unique()  # 验证是否存在
                    object_list.append(new_object)  # 验证通过, 存到列表中
                except Exception as e:
                    formset.errors[i].update(e)  # 如有有错误信息，存起来
                    generate_formset = formset
                    has_error = True
            if not has_error:  # 没有错误的时候，增加
                models.Permission.objects.bulk_create(object_list, batch_size=100)  # 批量增加数据，减小数据库开销
        else:
            generate_formset = formset

    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)  # extra 是否可以额外添加
    update_formset = None
    if request.method == 'POST' and post_type == 'update':
        formset = update_formset_class(data=request.POST)  # 获取提交过来的数据
        if formset.is_valid():  # 进行验证
            print(post_type)
            post_row_list = formset.cleaned_data  # 将数据存一份出来
            for i in range(0, formset.total_form_count()):  # 循环验证每一行数据，是否在数据库中存在
                row_dict = post_row_list[i]
                print(row_dict)
                permission_id = row_dict.pop('id')
                try:
                    row_object = models.Permission.objects.filter(id=permission_id).first()
                    for k, v in row_dict.items():
                        setattr(row_object, k, v)
                    row_object.validate_unique()  # 验证是否存在
                    row_object.save()  # 验证通过, 存到列表中
                except Exception as e:
                    formset.errors[i].update(e)  # 如有有错误信息，存起来
                    update_formset = formset

        else:
            update_formset = formset

    all_url_dict = get_all_url_dict()

    # 1、获取项目中所有的Url的值到一个集合
    router_name_set = set(all_url_dict)

    # 2、获取数据库中所有的url
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url',
                                                         'menu_id', 'menu__title',
                                                         'pid_id', 'pid__title',
                                                         'sort').order_by('name')
    permission_dict = OrderedDict()  # 有序字典
    permission_name_set = set()  # 集合
    for row in permissions:
        permission_dict[row['name']] = row
        permission_name_set.add(row['name'])

    # 3、添加、删除、修改的权限有哪些
    # 3.1 计算应该要增加的name  # 项目中有 数据库中没有
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set
        generate_formset = generate_formset_class(
            initial=[row_dict for name, row_dict in all_url_dict.items() if name in generate_name_list])
    # 3.2 计算应该要删除的name  # 数据库中有 项目中没有
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 3.3 应该要更新的name
    # 3.3.1 先检查一下 项目中的url与数据库中的url是否一样，
    for name, value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)  # 数据库中的name 是否存在于项目中
        if not router_row_dict:  # 如果不存在，不用管，会在要删除里面体现出来
            continue
        if value['url'] != router_row_dict['url']:  # 判断数据库中的url与项目中的url的值是否一致
            # print(value['url'], router_row_dict['url'])
            value['url'] = 'url与数据库中的不一致'

    update_name_list = permission_name_set & router_name_set  # 数据库和项目中都有 交集
    update_formset = update_formset_class(
        initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list])

    return render(request, 'rbac/multi_permissions.html',
                  {'generate_formset': generate_formset, 'delete_row_list': delete_row_list,
                   'update_formset': update_formset})
