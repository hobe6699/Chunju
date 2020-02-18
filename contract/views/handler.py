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
from stark.utils.get_custom_choice import get_datetime_text
from contract.models.signature import Signature, ContractUser
from django.utils.safestring import mark_safe
from django.urls import re_path, reverse
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

    def del_filter(self, obj=None, *args, **kwargs):
        if not obj:
            return False
        sig = Signature.objects.filter(name_id=obj.pk)
        if sig:
            return True
        return False

    def display_print(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return "打印"
        if obj:
            url = self.revers_url(self.get_print_url_name, pk=obj.pk)
            sig = Signature.objects.filter(name_id=obj.pk)
            if sig:
                return mark_safe(
                    "<a href='%s' target='_blank'><i class='fa fa-print fa-lg'></i></a>" % (url))
            return mark_safe(
                "<i class='fa fa-print fa-lg'></i>")

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
                sig_date = str(sig_date)[0:11]
                return render(request, self.print_template or 'stark/print.html/',
                              {'sig_img': sig_img, "cancel": url, "sig_date": sig_date})

        return redirect(url)  # 跳转回列表页面

    def sings_number(self):
        person_number = ContractUser.objects.all().count()
        person_id_list = ContractUser.objects.all().values_list('id')
        sing_list = Signature.objects.filter(name_id__in=person_id_list).values('name_id')
        sing_number = sing_list.distinct()
        sing_number.count()

        name = "%s:%s" % (self.site.namespace, self.get_list_url_name)
        base_url = reverse(name)
        sig_url = '%s?%s=%s' % (base_url, "custom_single_filter", 'sig')
        no_sig_url = '%s?%s=%s' % (base_url, "custom_single_filter", 'no_sig_url')

        return [{"person_number": person_number, "sing_number": sing_number.count(),
                 "no_sing_number": person_number - sing_number.count(), "all_url": base_url, "sig_url": sig_url,
                 "no_sig_url": no_sig_url}]

    def custom_single_search(self, request):
        custom_single_filter = request.GET.get('custom_single_filter')
        person_id_list = ContractUser.objects.all().values_list('id')
        sing_list = Signature.objects.filter(name_id__in=person_id_list).values('name_id')
        if custom_single_filter == "sig":
            return {'id__in': sing_list}
        if custom_single_filter == "no_sig_url":
            person_id_list = ContractUser.objects.exclude(**{"id__in": sing_list})
            return {'id__in': person_id_list}
        return {}

    extra_data = sings_number
    list_display = [StartHandler.display_checkbox, 'username', 'code', 'department', 'phone', display_is_sing]
    search_field_list = ['username__contains', 'code__contains', 'department__contains', 'phone__contains']
    list_template = 'contract/list.html'
    action_dict = {'action_multi_delete': '批量删除'}


class SignatureUserHandler(StartHandler):
    def display_department(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '部门'
        sig = Signature.objects.get(id=obj.pk)
        return mark_safe(sig.name.department)

    def display_code(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '工号'
        sig = Signature.objects.get(id=obj.pk)
        return mark_safe(sig.name.code)

    def display_phone(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '手机号'
        sig = Signature.objects.get(id=obj.pk)
        return mark_safe(sig.name.phone)

    search_field_list = ['name_id__username__contains', 'name_id__code__contains', 'name_id__department__contains',
                         'name_id__phone__contains']
    list_display = [StartHandler.display_checkbox, 'id', 'name', display_department, display_code, display_phone,
                    get_datetime_text('签名日期', 'create_date')]
    has_edit_btn = False
    list_template = 'contract/list_signature.html'
