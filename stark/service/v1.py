#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:23
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.db.models import manager
from django.shortcuts import render, HttpResponse
from django.urls import path, include, re_path


class StartHandler(object):
    def __init__(self, model_class):
        self.model_class = model_class

    def list_view(self, request):
        data_list = self.model_class.objects.all().values()
        return render(request, 'list.html', {"data_list": data_list})

    def add_view(self, request):
        return HttpResponse('添加视图')

    def change_view(self, request):
        return HttpResponse('修改视图')

    def delete_view(self, request):
        return HttpResponse('删除视图')

    def get_urls(self):
        patterns = [
            re_path(r'list/$', self.list_view),
            re_path(r'add/$', self.add_view),
            re_path(r'change/(\d+)/$', self.change_view),
            re_path(r'delete/(\d+)/$', self.delete_view),
        ]
        return patterns


class StarkSite(object):
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class=None, prev=None):
        """

        :param model_class: 是models中数据库相关的类
        :param handler_class: 是models中数据表的视图对象
        :param prev: 生成url的前缀
        :return:
        """
        if not handler_class:  # 如果没有定义视图函数 ，就用默认的
            handler_class = StartHandler

        self._registry.append(
            {'model_class': model_class, 'handler': handler_class(model_class)})  # 把model注册进来的目的，是对对应的表做增册改查

    def get_urls(self):
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']
            prev = item['prev']
            app_label, model_name = model_class._meta.app_label, model_class._meta.model_name
            if prev:
                patterns.append(
                    re_path(r'^%s/%s/%s/' % (app_label, model_name, prev), (handler.get_urls(), None, None)))

            else:
                patterns.append(re_path(r'^%s/%s/' % (app_label, model_name), (handler.get_urls(), None, None)))

        return patterns

    @property  # 将方法用属性的方式表示
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace


site = StarkSite()
