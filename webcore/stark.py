#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:22
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com
from stark.service.v1 import site, StartHandler, SearchOption
from stark.utils.get_custom_choice import get_choice_text
from webcore.models.organization import *


class OrgEmpHandler(StartHandler):
    list_display = [StartHandler.display_checkbox, StartHandler.display_id, 'org_info', 'org_dept', 'org_position',
                    'name',
                    get_choice_text('性别', 'gender'), 'account',
                    'wechat',
                    StartHandler.display_edit, StartHandler.display_del]
    has_search = True
    # search_list = ['org_info_name__contains', 'org_dept_name__contains', 'name__contains', 'org_dept_name__contains', ]
    action_dict = {'action_multi_delete': '批量删除'}

    # def get_list_display(self):
    #     return ['name', 'account',  StartHandler.display_edit,
    #                 StartHandler.display_del]
    search_group = [
        SearchOption('gender'),
        SearchOption('org_dept', {'id__gt': 0}),
        SearchOption('org_info', {'id__gt': 0}),
        SearchOption('account', {'id__gt': 0}),
    ]


site.register(OrgEmp, OrgEmpHandler)


class OrgInfoHandler(StartHandler):
    list_display = ['org_group', 'name', 'full_name', 'img', 'address', 'telephone', StartHandler.display_edit,
                    StartHandler.display_del]


site.register(OrgInfo, OrgInfoHandler)


# site.register(OrgInfo)
class OrgDeptHandler(StartHandler):
    list_display = ['org_info', 'parent', 'name', 'create_date', StartHandler.display_edit,
                    StartHandler.display_del]


site.register(OrgDept, OrgDeptHandler)

class OrgPositionHandler(StartHandler):
    search_group = [
        SearchOption('parent'),
        SearchOption('org_info'),
    ]
    has_search = True
    list_display = ['org_info','org_info', 'parent', 'name', 'create_date', StartHandler.display_edit,
                    StartHandler.display_del]

site.register(OrgPosition,OrgPositionHandler)