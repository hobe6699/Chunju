#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-10 10:50
# @Author  : mark.hu
# @Site    : www.ivan.net.cn
# @File    : rbac.py
# @Software: PyCharm

from django.template import (
    Library,
)
from django.conf import settings
from rbac.service import origin_url

register = Library()


@register.inclusion_tag('rbac/left_menu.html')  # 调用的模版
def left_menu(request):
    """
    创建菜单
    :return:
    """
    return {"menu_dict": request.session[settings.MENU_SESSION_KEY]}  # 给模版上的参数返回值


@register.filter
def has_permission(request, name):
    """
    判断按钮是否有权限
    :param request: 请求的信息
    :param name: url的别名
    :return:
    """
    if name in request.session[settings.PERMISSION_SESSION_KEY]:
        return True


@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的url (替代模板中的url)
    :param request:
    :param name:
    :return:
    """
    return origin_url.memory_url(request, name, *args, **kwargs)
