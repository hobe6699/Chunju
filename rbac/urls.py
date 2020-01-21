#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 13:10
# @Author  : mark.hu
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.urls import path, re_path
from rbac.views import role, user, menu, permission

app_name = 'rbac'
urlpatterns = [
    re_path(r'^role/list/$', role.role_list, name='rbac_role_list'),
    re_path(r'^role/add/$', role.role_add, name='rbac_role_add'),
    re_path(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name='rbac_role_edit'),
    re_path(r'^role/del/(?P<pk>\d+)/$', role.role_del, name='rbac_role_del'),
    # 用户
    re_path(r'^user/list/$', user.user_list, name='rbac_user_list'),
    re_path(r'^user/add/$', user.user_add, name='rbac_user_add'),
    re_path(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='rbac_user_edit'),
    re_path(r'^user/del/(?P<pk>\d+)/$', user.user_del, name='rbac_user_del'),
    re_path(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_password, name='rbac_user_reset_password'),
    # 一级菜单
    re_path(r'menu/list/', menu.menu_list, name='rbac_menu_list'),
    re_path(r'^menu/add/$', menu.menu_add, name='rbac_menu_add'),
    re_path(r'^menu/edit/(?P<pk>\d+)/$', menu.menu_edit, name='rbac_menu_edit'),
    re_path(r'^menu/del/(?P<pk>\d+)/$', menu.menu_del, name='rbac_menu_del'),

    # 二级菜单
    # menu_id 默认带过来一级菜单的ID
    re_path(r'^second/menu/add/(?P<menu_id>\d+)/$', menu.second_add, name='rbac_second_menu_add'),

    re_path(r'^second/menu/edit/(?P<pk>\d+)/$', menu.second_edit, name='rbac_second_menu_edit'),
    re_path(r'^second/menu/del/(?P<pk>\d+)/$', menu.second_del, name='rbac_second_menu_del'),

    # 权限菜单
    # menu_id 默认带过来一级菜单的ID
    re_path(r'^permission/add/(?P<second_mid>\d+)/$', permission.permission_add, name='rbac_permission_add'),

    re_path(r'^permission/edit/(?P<pk>\d+)/$', permission.permission_edit, name='rbac_permission_edit'),
    re_path(r'^permission/del/(?P<pk>\d+)/$', permission.permission_del, name='rbac_permission_del'),

    re_path(r'^multi/permissions/$', menu.multi_permissions, name='rbac_multi_permissions'),

]
