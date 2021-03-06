#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'mark'
__mtime__ = '2020-02-05'
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


def get_choice_text(title, field):
    """
    显示field 类型为choice的字段想要显示中文，可以用这个
    :param title: 显示的表头标题
    :param field: 字段名称
    :return:
    """

    def inner(self, obj=None, is_header=None):
        if is_header:
            return title
        method = "get_%s_display" % field

        return getattr(obj, method)

    return inner


def get_choice_index(model, field, value):
    """
    获取自定义的choice的索引
    :param model: 模版
    :param field: 字段名称
    :param value: 需要查询的值
    :return: 返回索引
    """
    t = getattr(model, '%s_choices' % field)
    for item in t:
        if item[1] == value:
            return item[0]
    return None


def get_choice_list(model, field):
    """
    返回自定义的choice的列表
    :param model: 模版
    :param field: 字段名称
    :return: 返回列表
    """
    try:
        t = getattr(model, '%s_choices' % field)
        if isinstance(t, tuple):
            return t
        return None
    except:
        return None


def get_datetime_text(title, field, time_format='d'):
    """
    显示field 定制时间格式
    :param title: 显示的表头标题
    :param field: 字段名称
    :param time_format: 时间格式  d:只显示日期，h:只显示时间，dh:显示日期和时间
    :return:
    """
    format = '%Y-%m-%d'
    if time_format == 'h':
        format = '%H:%m:%S'
    elif time_format == 'dh':
        format = '%Y-%m-%d %H:%m:%S'
    else:
        format = '%Y-%m-%d'

    def inner(self, obj=None, is_header=None):
        if is_header:
            return title
        datetime_value = getattr(obj, field)

        return datetime_value.strftime(format)

    return inner


def get_m2m_text(title, field):
    """
    显示field 类型为m2m的字段想要显示中文，可以用这个
    :param title: 显示的表头标题
    :param field: 字段名称
    :return:
    """

    def inner(self, obj=None, is_header=None):
        if is_header:
            return title
        queryset = getattr(obj, field)
        text_list = [str(row) for row in queryset]
        return ','.join(text_list)

    return inner
