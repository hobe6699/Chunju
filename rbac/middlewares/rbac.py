#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-09 11:21
# @Author  : mark.hu
# @Site    : www.ivan.net.cn
# @File    : rbac.py
# @Software: PyCharm

from django.utils.deprecation import MiddlewareMixin  # 中间件
from django.shortcuts import render
from django.conf import settings
import re
from django.urls import resolve
from rbac.service.origin_url import memory_reverse_url


class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当用户请求进来的时候执行
        :param request: # 请求的数据
        :return: # 返回None时，表示通过中间件验证
        """
        """
        1、获取当前用户请求的URL
        2、获取当前用户在session中保存的权限列表
        3、权限信息的匹配
        """
        current_url = request.path_info  # 获取请求url

        current_url_name = "%s:%s" % (resolve(request.path).namespace, resolve(request.path).url_name)  # 获取请求url的别名

        for valid_url in settings.VALID_URL_LIST:  # 验证白名单  当前请求的url如果在白名单中，直接跳过
            reg = "^{0}$".format(valid_url)  # 别名一致，跳过
            if current_url_name is not None:
                if re.match(valid_url, current_url_name):
                    return None
            if re.match(reg, current_url):  # url一致，跳过
                return None

        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)  # 从配置文件中获取权限session的key
        if not permission_dict:
            return render(request, 'error.html',
                          {"error_code": 401.1, "error_title": "权限错误", "error_content": "未获取到用户权限信息，请重新登陆!",
                           "a_name": "登陆",
                           "a_href": "/webcore/login/"})
        flag = False
        for url in permission_dict:
            reg = "^{0}$".format(url)
            if current_url_name is not None:
                if re.match(url, current_url_name):  # 别名一致，通协
                    flag = True
                    break
            if re.match(reg, current_url):  # url一致，通过
                flag = True
                break
        if not flag:
            return render(request, 'error.html',
                          {"error_code": 401.4, "error_title": "未授权", "error_content": "无权访问此页面，请联系管理员!",
                           "a_name": "登陆",
                           "a_href": "/webcore/login/"})
