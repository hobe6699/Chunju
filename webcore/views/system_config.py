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

from rbac.service.auto_register_permission import AutoRegisterPermission


def init_system_config(request):
    # url = routes.get_all_url_dict()
    # for k, v in url.items():
    #     print(k)
    AutoRegisterPermission('org', '组织权限', 'orgemp', '人员').init_permission()
    AutoRegisterPermission('org', '组织权限', 'orgemp', '人员').init_permission()
    AutoRegisterPermission('org', '组织权限', 'orgdept', '部门').init_permission()
    AutoRegisterPermission('org', '组织权限', 'orggroup', '组织').init_permission()
    AutoRegisterPermission('org', '组织权限', 'orginfo', '单位').init_permission()
    AutoRegisterPermission('rbac', '组织权限', 'role', '角色').init_permission()
    AutoRegisterPermission('rbac', '系统配置', 'rbac_menu', '菜单').init_permission()
    AutoRegisterPermission('rbac', '组织权限', 'rbac_second_menu', '二级菜单').init_permission()
    AutoRegisterPermission('rbac', '组织权限', 'permission', '权限').init_permission()
    AutoRegisterPermission('org', '组织权限', 'orgposition', '岗位').init_permission()
    AutoRegisterPermission('system_config', '系统配置', 'system_config', '权限初始化').init_permission()
    AutoRegisterPermission('webapp', '企业安全', 'area_class', '区域分类').init_permission()
    AutoRegisterPermission('webapp', '企业安全', 'area', '区域管理').init_permission()

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
