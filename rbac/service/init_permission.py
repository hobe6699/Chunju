#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-09 8:51
# @Author  : mark.hu
# @Site    : www.ivan.net.cn
# @File    : init_permission.py.py
# @Software: PyCharm
from django.conf import settings
from webcore.models.organization import OrgEmp


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user: 当前用户对像
    :param request: 请求相关的所有数据
    :return:
    """
    # 根据当前用户信息 获取此用户所拥有的所有权限 ，并放入session.
    permissions_queryset = current_user.roles.filter(permissions__isnull=False).values('permissions__id',
                                                                                       'permissions__title',
                                                                                       'permissions__url',
                                                                                       'permissions__name',
                                                                                       'permissions__pid',
                                                                                       'permissions__pid_id',
                                                                                       'permissions__pid__title',
                                                                                       'permissions__pid__url',
                                                                                       # 下面是从权限表再跨到一级菜单表中获取数据
                                                                                       'permissions__menu__id',
                                                                                       'permissions__menu__title',
                                                                                       'permissions__menu__icon',
                                                                                       'permissions__menu__sort').distinct().order_by('permissions__menu__sort','permissions__sort')

    # 获取权限 和 菜单信息
    menu_dict = {}  # 菜单列表
    permission_dict = {}  # 权限列表
    for item in permissions_queryset:
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__pid_id'],
            'p_title': item['permissions__pid__title'],
            'p_url': item['permissions__pid__url'],
        }  # 获取权限中所有的url

        menu_id = item['permissions__menu__id']  # 生成菜单 1、权限表中的数据行是否有一级菜单ID
        if not menu_id:  # 2、如果没有 进行下一个循环
            continue
        # 如果有
        node = {'title': item['permissions__title'], 'url': item['permissions__url']}  # 获取权限表中的数据行
        if menu_id in menu_dict:  # 3、菜单ID是否在菜单字典中
            menu_dict[menu_id]['children'].append(node)  # 3.1、将 权限表中的数据行，放入菜单的children中做为二级菜单
        else:  # 3.2 如果不存在，构建菜单数据字典
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'sort': item['permissions__menu__sort'],
                'children': [node, ]
            }
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict


