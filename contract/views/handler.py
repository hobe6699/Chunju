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
from django.urls import re_path
from django.shortcuts import render, redirect


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

    def display_print(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return "打印"
        if obj:
            url = self.revers_url(self.get_print_url_name, pk=obj.pk)
            return mark_safe(
                "<a href='%s' target='_blank'><i class='fa fa-print fa-lg'></i></a>" % (url))

    print_template = "sig_print.html"

    @property  # 将方法以属性的方式表示
    def get_print_url_name(self):
        """
        :return: 生成删除url名称
        """
        return self.get_url_name('print')

    def extra_urls(self):
        """
        :return: 用于增加额外的路由
        """
        return [re_path(r'^print/(?P<pk>\d+)/$', self.wrapper(self.print_view), name=self.get_print_url_name),
                ]

    def print_view(self, request, pk, *args, **kwargs):
        url = self.reverse_list_url(*args, **kwargs)
        if request.method == "GET":
            obj = ContractUser.objects.filter(id=pk).values('username', 'signature__signature',
                                                            'signature__create_date')
            if obj:
                for item in obj:
                    sig_img = item['signature__signature']
                    sig_date = item['signature__create_date']
                sig_date = str(sig_date)[0:19]
                return render(request, self.print_template or 'stark/print.html/',
                              {'sig_img': sig_img, "cancel": url, "sig_date": sig_date})

        return redirect(url)  # 跳转回列表页面

    def display_show_sing(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '签名'
        sig = Signature.objects.filter(name_id=obj.pk).all()
        if sig:
            lab = "<img src='%s' style='width:95px; height:80px'>" % sig[0].signature
        else:
            lab = "<label class='label badge-danger'>None</label>"
        return mark_safe(lab)

    def sings_number(self):
        person_number = ContractUser.objects.all().count()
        person_id_list = ContractUser.objects.all().values_list('id')

        sing_list = Signature.objects.filter(name_id__in=person_id_list).values('name_id')
        sing_number = sing_list.distinct()
        sing_number.count()
        return [{"person_number": person_number, "sing_number": sing_number.count(),
                 "no_sing_number": person_number - sing_number.count()}]

    extra_data = sings_number
    list_display = ['username', 'code', 'department', 'phone', display_is_sing, display_print]
    list_template = 'contract/list.html'
    has_del_btn = False
    has_search = True


class SignatureUserHandler(StartHandler):
    list_display = ['name']
