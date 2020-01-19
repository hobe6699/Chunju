#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/10 13:51
# @Author  : mark.hu
# @Site    : 
# @File    : ent_login.py
# @Software: PyCharm
# @Emial:5898387@qq.com
from django.shortcuts import HttpResponse, redirect
from rbac.models import UserInfo
from rbac.service.init_permission import init_permission
from webapp.views.tencent import ent_wechat_signature
import json
from urllib.parse import unquote
from django.views.decorators.csrf import csrf_exempt, csrf_protect


@csrf_exempt
def get_authorize_url(request):
    redirect_url = "http://" + request.get_host() + "/webapp/oauth_user/"
    client = ent_wechat_signature.BaseAuthorization.get_access_client()
    url = client.oauth.authorize_url(redirect_url)
    return redirect(url)


@csrf_exempt
def oauth_user(request):
    code = request.GET['code'] if 'code' in request.GET else None
    client = ent_wechat_signature.BaseAuthorization.get_access_client()  # 获取接入的微信用户
    if code:
        wechat_user_id = request.session.get("wechat_user_id")  # 从缓存中获取用户的微信ID
        if not wechat_user_id:  # 如果不存在
            user_info = client.oauth.get_user_info(code)  # 从访问的客户端中获取ID
            wechat_user_id = user_info['UserId']
            request.session['wechat_user_id'] = user_info['UserId']  # 存入缓存
        current_user = UserInfo.objects.filter(name=wechat_user_id).first()  # 获取用户信息
        if not current_user:
            return HttpResponse("没有授权的用户信息")
        init_permission(current_user, request)  # 调用权限初始化
        return redirect('/webapp/inspect/')


@csrf_exempt
def verify(request):
    request_type = request.POST.get('type')
    if not request_type:
        request_body = json.loads(request.body.decode())
        pathname = request_body['url']
        # print(unquote(pathname))
        sign = ent_wechat_signature.signature(unquote(pathname))
        sign = json.dumps(sign.sign())
        # print(sign)
        return HttpResponse(sign, content_type="application/json")
