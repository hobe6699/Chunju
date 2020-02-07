#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-20 9:01
# @Author  : mark.hu
# @Site    : www.ivan.net.cn
# @File    : wechat.py
# @Software: PyCharm
from django.conf import settings
from wechatpy.enterprise import WeChatClient
from django.core.cache import cache
from django.views.generic import View
import random, string, time
from webapp.models.tencent.ent_wechat_conf import *
from django.views.decorators.csrf import csrf_exempt

# try:
#     wechat_app = EntWechatConf.objects.values().first()
#     corp_id = wechat_app['corp_id']  # 企业ID
#     app_id = wechat_app['app_id']  # 应用ID
#     app_secret = wechat_app['app_secret']  # 应用秘钥
# except Exception:

corp_id = settings.CORP_ID
app_id = settings.APP_ID
app_secret = settings.APP_SECRET


class BaseAuthorization():
    @classmethod
    def get_ticket(cls):
        key = 'ticket'
        if cache.has_key(key):
            ticket = cache.get(key)
        else:
            if cache.has_key('client'):
                client = cache.get('client')
            else:
                client = BaseAuthorization.get_access_client()
            ticket = client.jsapi.get_jsapi_ticket()
            cache.set(key, ticket, 110 * 60)
        return ticket

    @staticmethod
    def get_access_client():
        key = 'client'
        if cache.has_key(key):
            client = cache.get(key)
        else:
            client = WeChatClient(corp_id, app_secret)
            cache.set(key, client)
        return client


@csrf_exempt
class signature(View):
    def __init__(self, url):
        self.client = BaseAuthorization.get_access_client()
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': self.client.jsapi.get_ticket()['ticket'],
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        self.ret['signature'] = self.client.jsapi.get_jsapi_signature(self.ret['nonceStr'], self.ret['jsapi_ticket'],
                                                                      self.ret['timestamp'],
                                                                      self.ret['url'])
        return self.ret
