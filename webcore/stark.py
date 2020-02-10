#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:22
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com
from stark.service.v1 import site

from webcore.views.organization.organization import *

site.register(OrgGroup, OrgGroupHandler)

site.register(OrgInfo, OrgInfoHandler)

site.register(OrgDept, OrgDeptHandler)

site.register(OrgPosition, OrgPositionHandler)

site.register(OrgEmp, OrgEmpHandler)
