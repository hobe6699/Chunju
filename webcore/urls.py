#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/8 15:20
# @Author  : mark.hu
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @Emial:5898387@qq.com
from django.urls import path, re_path
from webcore.views import *

app_name = 'webcore'
urlpatterns = [
    re_path(r"^login/$", account.login, name="webcore_login"),

    re_path(r"^logout/$", account.logout, name="webcore_logout"),
    re_path(r"^error/$", account.error, name="webcore_error"),
    re_path(r"^init_system_config/$", system_config.init_system_config, name="webcore_init_system_config"),
    re_path(r"^index/$", home.index, name="webcore_index"),
    re_path(r"^index_v1/$", home.index_v1, name="webcore_index_v1"),
    re_path(r"^layout/$", home.layout, name="webcore_layout"),
    re_path(r"^success/$", home.success, name="webcore_success"),
    re_path(r'^WW_verify_83z6GYOPGCfBqcDy.txt', ent_wachat_verify.ent_wachat_verify, name='WW_verify_83z6GYOPGCfBqcDy'),
    # 组织
    re_path(r'^group/list/$', orggroup.group_list, name='group_list'),
    re_path(r'^group/add/$', orggroup.group_add, name='group_add'),
    re_path(r'^group/edit/(?P<pk>\d+)/$', orggroup.group_edit, name='group_edit'),
    re_path(r'^group/del/(?P<pk>\d+)/$', orggroup.group_del, name='group_del'),

]
