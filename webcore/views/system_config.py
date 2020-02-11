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
from django.shortcuts import render, redirect, HttpResponse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import OperationalError, Error
from rbac.service import routes
from rbac.models import Menu, Permission, Role

from django.core.serializers import serialize
import json


def init_system_config(request):
    url = routes.get_all_url_dict()

    for k, v in url.items():
        if 'list' in str(k):
            pass
        if 'org' in str(k):
            menu_id = check_menu('组织权限')
            print(menu_id)
            if 'list' in str(k):
                name = v['name']
                url = v['url']
                print(name, url)
                check_permission(name=name, url=url, title='组织%s' % name, menu_id=menu_id)

            else:
                print('---')
                name = v['name']
                url = v['url']
                print(name, url)

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


def check_menu(name):
    obj = Menu.objects.filter(title=name).all()
    if not obj:
        Menu.objects.create(title=name, icon='fa-th')
        obj = Menu.objects.filter(title=name).all()
    menu = json.loads(serialize('json', obj))
    pk = menu[0]['pk']
    return pk


def check_permission(name, url, title, pid=None, menu_id=None):
    if menu_id:
        obj = Permission.objects.filter(name=name)
        if not obj:
            Permission.objects.create(name=name, title=title, url=url, menu_id=menu_id)
            obj = Permission.objects.filter(name=name)
            return obj
        return obj
    else:
        obj = Permission.objects.filter(name=name)
        if not obj:
            Permission.objects.create(name=name, title=title, url=url, pid=pid)
            obj = Permission.objects.filter(name=name)
            return obj
        return obj


def check_system_admin():
    obj = Role.objects.filter(title='admin')
    if not obj:
        obj = Role.objects.create(title='admin')
    return obj
