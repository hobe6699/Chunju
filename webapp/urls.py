#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-01-02 13:58
# @Author  : mark.hu
# @Site    : www.ivan.net.cn
# @File    : url.py
# @Software: PyCharm

from django.urls import path, re_path
from webapp.views import *

app_name = 'webapp'
urlpatterns = [

    re_path(r'^ent_wechat_conf/$', ent_wechat_conf.ent_wechat_conf, name="webapp_ent_wechat_conf"),  # 企业微信配置
    re_path(r'^ent_wechat_conf/add/$', ent_wechat_conf.ent_wechat_conf, name="webapp_ent_wechat_conf_add"),
    # 企业微信配置---添加
    re_path(r"content/", ent_wechat_replay_msg.replay_msg, name="webapp_content"),  # 接收企业微信发送的消息 并处理
    re_path(r'verify/', ent_oauth.verify, name="webapp_verify"),  # 登入第一步，unquote需要验证的地址
    re_path(r'entwxlogin/', ent_oauth.get_authorize_url, name="webapp_entwxlogin"),  # 登入第二步，请求用户code 并跳转到指定的网页
    re_path(r'^oauth_user/', ent_oauth.oauth_user, name="webapp_oauth_user"),  # 登录第三步，获取到用户信息 并存入session
    re_path(r"^inspect/", safety.inspect, name="webapp_inspect"),  # 登录第四步，跳转到指定的页面
    re_path(r'^inspect_form/', safety.inspect_form, name="webapp_inspect_form"),  # 报告页面
    re_path(r'upload_img/', upload_files.upload_img, name="webapp_upload_img"),  # 上传图片
    re_path(r'upload_img_del/', upload_files.upload_img_del, name="webapp_upload_img_del"),  # 删除图片
    re_path(r'check_record/', safety.check_record, name="webapp_check_record"),  # 检查记录页面

    # 区域分类设置
    re_path(r'^area/class/list/$', area_class.area_class_list, name='area_class_list'),
    re_path(r'^area/class/add/$', area_class.area_class_add, name='area_class_add'),
    re_path(r'^area/class/edit/(?P<pk>\d+)/$', area_class.area_class_edit, name='area_class_edit'),
    re_path(r'^area/class/del/(?P<pk>\d+)/$', area_class.area_class_del, name='area_class_del'),

    # 区域设置
    re_path(r'^area/list/$', area.area_list, name='area_list'),
    re_path(r'^area/add/(?P<acid>\d+)/$', area.area_add, name='area_add'),
    re_path(r'^area/edit/(?P<pk>\d+)/$', area.area_edit, name='area_edit'),
    re_path(r'^area/del/(?P<pk>\d+)/$', area.area_del, name='area_del'),

]
