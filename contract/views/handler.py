#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'mark'
__mtime__ = '2020-02-13'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from stark.service.v1 import StartHandler, SearchOption, StarkModelForm, StarkForm
from contract.models.signature import Signature, ContractUser
from django.utils.safestring import mark_safe


class ContractUserHandler(StartHandler):

    def display_is_sing(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '是否签名'
        print(obj.pk)
        sig = Signature.objects.filter(name_id=obj.pk)
        if sig:
            lab = "<label class='label badge-success'>是</label>"
        else:
            lab = "<label class='label badge-danger'>否</label>"
        return mark_safe(lab)

    list_display = ['username', 'code', 'department', 'phone', display_is_sing]
    list_template = 'contract/list.html'


class SignatureUserHandler(StartHandler):
    list_display = ['name']
