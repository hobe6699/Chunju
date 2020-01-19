#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/13 13:01
# @Author  : mark.hu
# @Site    : 
# @File    : sysconf.py
# @Software: PyCharm
# @Emial:5898387@qq.com
from django.shortcuts import render, HttpResponse
from webapp.models.tencent.ent_wechat_conf import *


def ent_wechat_conf(request):
    # wechat_app = EntWechatConf.objects.values().first()
    # print(wechat_app['id'])
    ewc = EntWechatConf.objects.all()
    return render(request, 'tencent/ent_wechat_conf.html', {"ewc": ewc})
