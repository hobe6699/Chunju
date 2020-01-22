#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:22
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com
from stark.service.v1 import site, StartHandler
from webcore.models.organization import *


class OrgEmpHandler(StartHandler):
    pass


site.register(OrgEmp, OrgEmpHandler)
site.register(OrgGroup)
# site.register(OrgInfo)
# site.register(OrgPosition)
# site.register(OrgDept)
