#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:23
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.db import models


class ContractUser(models.Model):
    code = models.CharField(verbose_name='工号', max_length=64, null=True)
    username = models.CharField(verbose_name='姓名', max_length=256)
    department = models.CharField(verbose_name='部门', max_length=128, null=True, blank=True)
    group = models.CharField(verbose_name='所', max_length=128, null=True, blank=True)
    phone = models.CharField(verbose_name='手机号', max_length=32, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'contract'
        db_table = 'contract_contract_user'


class Signature(models.Model):
    name = models.ForeignKey(to=ContractUser, on_delete=models.CASCADE, verbose_name='签字人', null=True)
    signature = models.TextField(verbose_name='签名', blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='签名时间')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'contract'
        db_table = 'contract_signature'
