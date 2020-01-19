#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/19 10:22
# @Author  : mark.hu
# @Site    : 
# @File    : routes.py
# @Software: PyCharm
# @Email:5898387@qq.com
import re
from collections import OrderedDict  # 有序字典
from django.conf import settings
from django.utils.module_loading import import_string  # 根据字符串的型导入模块
from django.urls import URLPattern, URLResolver


def get_all_url_dict():
    """
    获取项目中所有的url( url必须的别名 name)
    :return:
    """
    url_ordered_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)  # 根据字符串的型导入模块  == from Chunju import urls
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)  # 递归的去获取所有URL
    return url_ordered_dict


def recursion_urls(per_namespace, per_url, urlpatterns, url_ordered_dict):
    """
    递归的去获取URL
    :param per_namespace: url中的namespace ,用于拼接name
    :param per_url: url的前缀 ，用于拼接url
    :param urlpatterns:  路由关系列表
    :param url_ordered_dict:  用于保存递归中获取的所有路由
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, URLPattern):  # 非路由分发，就是没有include,是最后一级的路由了，就将路由添加到url_ordered_dict
            if not item.name:  # 如果url 没有别名name ,不管它
                continue
            # if per_namespace:  # url中的namespace 有就拼接
            #     name = "%s_%s" % (per_namespace, item.name)
            # else:
            name = item.name
            url = per_url + str(item.pattern)  # 拼接路由
            url = url.replace('^', '').replace('$', '')  # 去掉正则符号

            if check_url_exclude(url):  # 排除一些特定的url
                continue

            url_ordered_dict[name] = {"name": name, "url": url}
        elif isinstance(item, URLResolver):  # 是路由 有include 继续递归操作
            if per_namespace:  # 多级路由分发时，拼接  如"rbac:admin:/xxxx/xxxx"
                if item.namespace:  # 父级有，子级有 rbac:admin:/xxxx/xxxx
                    namespace = "%s:%s" % (per_namespace, item.namespace)
                else:  # 父级有 子级没有 rbac:/xxxx/xxxx
                    namespace = item.namespace
            else:
                if item.namespace:  # 父级没有 子级有 admin:/xxxx/xxxx
                    namespace = item.namespace
                else:  # 都没有 /xxxx/xxxx
                    namespace = None
            url = per_url + str(item.pattern)  # 拼接路由

            recursion_urls(namespace, url, item.url_patterns, url_ordered_dict)


def check_url_exclude(url):
    """
    排除一些特定的Url
    :param url: 要排的url
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True
