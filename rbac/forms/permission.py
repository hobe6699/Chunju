#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/16 15:13
# @Author  : mark.hu
# @Site    : 
# @File    : menu.py
# @Software: PyCharm
# @Email:5898387@qq.com

from rbac import models
from rbac.forms.base import BootStrapModelForm  # 基础样式


class PermissionModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        exclude = ['menu']
