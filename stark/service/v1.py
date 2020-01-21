#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:23
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com

class StarkSite(object):
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class):
        """

        :param model_class: 是models中数据库相关的类
        :return:
        """

        self._registry.append({'model_class': model_class})  # 把model注册进来的目的，是对对应的表做增册改查
        """
        [
            {"model_class":OrgEmp}
            {"model_class":OrgGroup}
            {"model_class":OrgInfo}
        ]        
        """


site = StarkSite()
