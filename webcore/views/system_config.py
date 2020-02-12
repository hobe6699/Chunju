#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'mark'
__mtime__ = '2020-02-11'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from django.shortcuts import render

from rbac.service import routes
from rbac.models import Menu, Permission, Role

from django.core.serializers import serialize
import json
from django.db.models import Q

l = [{'org': {'menu_name': '组织权限',
              'permission': [{'orgemp': '人员'}, {'orgdept': '部门'}, {'orggroup': '单位'}, {'orginfo': '单位'},
                             {'orgposition': '岗位'}]}}]


def get_permission_list(select_str, menu_name, table_name, table_title):
    menu_list = dict()

    menu_list["select_str"] = select_str
    menu_list["menu_name"] = menu_name
    menu_list["table_name"] = table_name
    menu_list["table_title"] = table_title
    return menu_list


from rbac.service.auto_register_permission import AutoRegisterPermission


def init_system_config(request):
    AutoRegisterPermission('org', '组织权限', 'orgemp', '人员').init_permission()
    AutoRegisterPermission('org', '组织权限', 'orgdept', '部门').init_permission()
    # print(settings.DATABASES)
    # init_database_name = 'test02'
    # print(request.GET)
    # conn = ''
    # try:
    #     conn = psycopg2.connect(database="postgres", user="mark", host="127.0.0.1", port="5432")
    # except OperationalError as e:
    #     print("aaaa")
    #     print(e)
    #     if "connections" in str(e):
    #         return HttpResponse('数据库地址或端口错误,无法连接到数据库.')
    #     if 'role' in str(e):
    #         return HttpResponse('用户名错误!')
    #     if 'database' in str(e):
    #         return HttpResponse('postgres数据库不存在!')
    #
    #     return HttpResponse('用户名不正确!')
    #
    # try:
    #     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    #     print(conn.closed)
    #     cursor = conn.cursor()
    #     print('open')
    #     print(cursor)
    #     cursor.execute("CREATE DATABASE {}".format(init_database_name))
    #     cursor.close()
    #     conn.close()
    #     print(cursor)
    #     print(conn)
    # except Error as e:
    #     if 'database "%s" already exists' % init_database_name in str(e):
    #         return HttpResponse('数据库已存在!')

    return render(request, 'init_system_config.html')


def init_permission():
    url = routes.get_all_url_dict()
    menu_list = get_permission_list('org', '组织权限', 'orgemp', '人员')
    select_str = menu_list["select_str"]
    menu_name = menu_list["menu_name"]
    table_name = menu_list["table_name"]
    table_title = menu_list["table_title"]
    for k, v in url.items():
        print(k)
        name = v['name']
        url = v['url']
        if select_str in str(k):
            menu_id = check_menu(menu_name)
            if table_name in str(k):
                add_permission(name_class=table_name, name=name, url=url, menu_id=menu_id, title=table_title)


def add_permission(name_class, name, url, menu_id, title):
    name = name
    url = url
    if name_class in name and 'add' in name:
        pid = check_permission_is_menu(name_class, 'list')
        check_permission(name=name, url=url, title='%s_添加' % title, pid=pid)
    if name_class in name and 'change' in name:
        pid = check_permission_is_menu(name_class, 'list')
        check_permission(name=name, url=url, title='%s_编辑' % title, pid=pid)
    if name_class in name and 'delete' in name:
        pid = check_permission_is_menu(name_class, 'list')
        check_permission(name=name, url=url, title='%s_删除' % title, pid=pid)
    if name_class in name and 'list' in name:
        check_permission(name=name, url=url, title='%s' % title, menu_id=menu_id)


def check_menu(name):
    """
    检查一级菜单是否存在，存在返回pk ,不存在添加并返回pk
    :param name: 菜单标题
    :return: 对应的pk
    """
    obj = Menu.objects.filter(title=name).all()
    if not obj:
        Menu.objects.create(title=name, icon='fa-th')
        obj = Menu.objects.filter(title=name).all()
    menu = json.loads(serialize('json', obj))
    pk = menu[0]['pk']
    return pk


def check_permission_is_menu(name, pams):
    """
    检查二级菜单是否存在
    :param pams1:名称
    :param pams2:类型
    :return:
    """
    obj = Permission.objects.filter(Q(name__contains=name) & Q(name__contains=pams))
    pk = None
    if obj:
        permission = json.loads(serialize('json', obj))
        pk = permission[0]['pk']
    return pk


def check_permission(name, url, title, pid=None, menu_id=None):
    """
    创建权限
    :param name: 路径别名
    :param url: url
    :param title:标题
    :param pid: 父级id
    :param menu_id: 菜单ID
    :return: pk
    """
    if menu_id:
        obj = Permission.objects.filter(name=name)
        if not obj:
            Permission.objects.create(name=name, title=title, url=url, menu_id=menu_id)
            obj = Permission.objects.filter(name=name)
    else:
        obj = Permission.objects.filter(name=name)
        if not obj:
            Permission.objects.create(name=name, title=title, url=url, pid_id=pid)
            obj = Permission.objects.filter(name=name)
    if obj:
        p_obj = Permission.objects.get(name=name)
        check_system_admin(p_obj)
    return obj


def check_system_admin(p_obj):
    """
    检查系统管理员是否存在
    :return: pk
    """
    obj = Role.objects.filter(title='admin')
    if not obj:
        Role.objects.create(title='admin')
    r_obj = Role.objects.get(title='admin')
    rp = Role.objects.filter(title='admin', permissions=p_obj).exists()
    if not rp:
        r_obj.permissions.add(p_obj)
