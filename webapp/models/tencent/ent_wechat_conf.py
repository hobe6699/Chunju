#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/13 13:05
# @Author  : mark.hu
# @Site    : 
# @File    : ent_wechat_conf.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.db import models


class EntWechatConf(models.Model):
    name = models.CharField(max_length=64, verbose_name="应用名称")
    corp_id = models.CharField(max_length=64, verbose_name="企业ID")
    app_id = models.CharField(max_length=64, verbose_name="应用ID")
    app_secret = models.CharField(max_length=128, verbose_name="应用Secret")
    token = models.CharField(max_length=64, verbose_name="应用token", help_text='应用的 接收消息服务器的Token')
    encoding_aes_key = models.CharField(max_length=64, verbose_name="应用EncodingAESKey")

    class Meta:
        db_table = "ent_wechat_conf"


class LocationLog(models.Model):
    name = models.CharField(max_length=64, verbose_name="微信用户名")
    create_date = models.CharField(max_length=64, verbose_name="接收时间")
    latitude = models.FloatField(verbose_name="纬度")
    longitude = models.FloatField(verbose_name="经度")
    precision = models.FloatField(verbose_name="精度")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ent_wechat_location_log"


class MessageTemplate(models.Model):
    name = models.CharField(max_length=64, verbose_name="模版名称")
    agent_id = models.CharField(max_length=64, verbose_name="企业应用id")  # 企业应用的id
    user_ids = models.CharField(max_length=2048, verbose_name="接收消息成员列表", null=True, blank=True)
    party_ids = models.CharField(max_length=2048, verbose_name="接收消息部门列表", null=True, blank=True)
    tag_ids = models.CharField(max_length=2048, verbose_name="接收消息标签列表", null=True, blank=True)
    msg_type = models.CharField(max_length=64, verbose_name="消息类型")
    title = models.CharField(max_length=64, verbose_name="标题", null=True, blank=True)
    description = models.TextField(max_length=2048, verbose_name="内容")
    url = models.CharField(max_length=64, verbose_name="路径", null=True, blank=True)
    btntxt = models.CharField(max_length=64, verbose_name="底部文字", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ent_wechat_message_template"
