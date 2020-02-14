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
        sig = Signature.objects.filter(name_id=obj.pk)
        if sig:
            lab = "<label class='label badge-success'>是</label>"
        else:
            lab = "<label class='label badge-danger'>否</label>"
        return mark_safe(lab)

    def display_show_sing(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '签名'
        sig = Signature.objects.filter(name_id=obj.pk)
        if sig:
            signature_img = Signature.objects.get(name_id=obj.pk)
            lab = "<img src='%s' style='width:95px; height:80px'>" % signature_img.signature
        else:
            lab = "<label class='label badge-danger'>None</label>"
        return mark_safe(lab)

    def sings_number(self):
        person_number = ContractUser.objects.all().count()
        person_id_list = ContractUser.objects.all().values_list('id')
        sing_number = Signature.objects.filter(name_id__in=person_id_list).count()

        return [{"person_number": person_number, "sing_number": sing_number,
                 "no_sing_number": person_number - sing_number}]

    extra_data = sings_number
    list_display = ['username', 'code', 'department', 'phone', display_is_sing, display_show_sing]
    list_template = 'contract/list.html'
    has_del_btn = False
    has_search = True


class SignatureUserHandler(StartHandler):
    list_display = ['name']
