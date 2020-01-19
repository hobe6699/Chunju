#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/13 14:07
# @Author  : mark.hu
# @Site    : 
# @File    : ent_replay_msg.py
# @Software: PyCharm
# @Email:5898387@qq.com
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy import parse_message, create_reply
from wechatpy.replies import TextReply, ArticlesReply
from wechatpy.events import ScanCodePushEvent, LocationEvent
from django.conf import settings
from django.shortcuts import HttpResponse
from webapp.models.tencent.ent_wechat_conf import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect


@csrf_exempt  # @csrf_exempt 此装饰器用于取消 csrf验证
def replay_msg(request):
    wechat_app = EntWechatConf.objects.values().first()
    token = wechat_app['token']  # 访问令牌
    encoding_aes_key = wechat_app['encoding_aes_key']  # 应用EncodingAESKey
    corp_id = wechat_app['corp_id']  # 企业ID
    signature = request.GET.get('msg_signature', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
    echo_str = request.GET.get('echostr', '')
    crypto = WeChatCrypto(token, encoding_aes_key, corp_id)
    if request.method == 'GET':
        try:
            secho_str = crypto.check_signature(signature, timestamp, nonce, echo_str)
        except InvalidSignatureException:
            raise
        return HttpResponse(secho_str)
    raw_message = request.body
    try:
        decrypted_xml = crypto.decrypt_message(raw_message, signature, timestamp, nonce)
    except (InvalidSignatureException, InvalidCorpIdException):
        raise
    else:
        msg = parse_message(decrypted_xml)
        if msg.type == 'event':
            if msg.event == 'location':
                # from webapp.views.tencent.message_template import replay_msg
                # replay_msg()
                # 把位置信息存入数据库中
                try:
                    LocationLog.objects.create(
                        **{"name": msg.source, "create_date": msg.create_time, "latitude": msg.latitude,
                           "longitude": msg.longitude, "precision": msg.precision})
                except Exception as e:
                    print(e)

                reply = TextReply(content="", message=msg)
                xml = reply.render()
                encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)
                return HttpResponse(encrypted_xml)
            if msg.event == 'scancode_push':
                m = ScanCodePushEvent(msg)
                print(m)
                reply = TextReply(content=m.scan_result, message=msg)
                xml = reply.render()
                encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)
                return HttpResponse(encrypted_xml)
            if msg.event == 'view':
                print(msg.source)
                reply = TextReply(content="", message=msg)
                xml = reply.render()
                encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)
                return HttpResponse(encrypted_xml)
        if msg.type == 'text' or msg.type == 'enter_agent':
            reply = TextReply(content="谢谢", message=msg)
            xml = reply.render()
            encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)
            return HttpResponse(encrypted_xml)
        if msg.type == 'unknown':
            reply = TextReply(content="", message=msg)
            xml = reply.render()
            encrypted_xml = crypto.encrypt_message(xml, nonce, timestamp)
            return HttpResponse(encrypted_xml)
