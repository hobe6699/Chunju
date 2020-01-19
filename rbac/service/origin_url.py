#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/16 17:16
# @Author  : mark.hu
# @Site    : 
# @File    : origin_url.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.urls import reverse
from django.http import QueryDict  # 主要是为了解决请求中一个key对应多个value的问题，


def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的url (替代模板中的url)
    :param request:
    :param name:
    :return:
    """

    basic_url = reverse(name, args=args, kwargs=kwargs)

    # 判断当前url中是否有参数
    if not request.GET:
        return basic_url
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()  # 获取URl中的参数 给到_filter
    return "%s?%s" % (basic_url, query_dict.urlencode())


def memory_reverse_url(request, name, *args, **kwargs):
    """
    反向生成url
    :param request:请求
    :param name: 要返回的url 名称
    :param args: 参数
    :param kwargs:  参数
    :return:
    """
    url = reverse(name, args=args, kwargs=kwargs)
    origin_params = request.GET.get('_filter')
    if origin_params:
        url = "%s?%s" % (url, origin_params)
    return url
