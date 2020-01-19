#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/13 15:35
# @Author  : mark.hu
# @Site    : 
# @File    : message_template.py
# @Software: PyCharm
# @Email:5898387@qq.com
from wechatpy.enterprise.client.api import WeChatMessage
from webapp.views.tencent import ent_wechat_signature
from webapp.models.tencent.ent_wechat_conf import *
from webapp.templates.tencent import *


class MessageTemplate:
    def __init__(self, template_name, content=None):
        self.template_name = template_name
        self.content = content

    def replay_msg(self):
        client = ent_wechat_signature.BaseAuthorization.get_access_client()
        message_template = MessageTemplate.objects.filter(name=self.template_name).values()
        if not self.content:
            self.content = message_template[0]["description"]

        if message_template:
            if message_template[0]["msg_type"] == 'card':
                client.message.send_text_card(agent_id=message_template[0]["agent_id"],
                                              user_ids=message_template[0]["user_ids"],
                                              title=message_template[0]["user_ids"],
                                              description=self.content,
                                              url=message_template[0]["url"],
                                              btntxt=message_template[0]["btntxt"],
                                              party_ids=message_template[0]["party_ids"],
                                              tag_ids=message_template[0]["tag_ids"])
            if message_template[0]["msg_type"] == 'markdown':
                client.message.send_markdown(agent_id=message_template[0]["agent_id"],
                                             user_ids=message_template[0]["user_ids"],
                                             content=self.content,
                                             party_ids=message_template[0]["party_ids"],
                                             tag_ids=message_template[0]["tag_ids"])
