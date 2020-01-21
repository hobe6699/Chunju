#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/16 15:13
# @Author  : mark.hu
# @Site    : 
# @File    : menu.py
# @Software: PyCharm
# @Email:5898387@qq.com

from rbac import models
from django import forms
from django.utils.safestring import mark_safe  # 让样式显示出来，表示是安全的字符
from rbac.forms.base import BootStrapModelForm

# 图标、可以放到数据库中去读出来
ICON_LIST = [['fa-adjust', mark_safe('<i class="fa fa-adjust" aria-hidden="true"></i>')],
             ['fa-binoculars', mark_safe('<i class="fa fa-binoculars" aria-hidden="true"></i>')],
             ['fa-bar-chart', mark_safe('<i class="fa fa-bar-chart" aria-hidden="true"></i>')],
             ['fa-barcode', mark_safe('<i class="fa fa-barcode" aria-hidden="true"></i>')], ]


class MenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = ['title', 'icon']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
                   'icon': forms.RadioSelect(choices=ICON_LIST)}


class SecondMenuModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        exclude = ['pid']


class MultiAddPermissionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control input-sm'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control input-sm'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control input-sm'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        required=False,
    )
    pid = forms.ChoiceField(
        choices=[(None, '-----')],
        required=False,
    )

    sort = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}),
        required=False,
        initial=999,  # 默认值

    )

    def __init__(self, *args, **kwargs):
        super(MultiAddPermissionForm, self).__init__(*args, **kwargs)
        # 生成选择列表
        self.fields["menu_id"].choices += models.Menu.objects.values_list('id', 'title')
        self.fields["menu_id"].widget.attrs['class'] = 'form-control input-sm'
        # 当pid为空 menu不为空时  表示可以做菜单的选择项
        self.fields['pid'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')
        self.fields["pid"].widget.attrs['class'] = 'form-control input-sm'


class MultiEditPermissionForm(forms.Form):
    id = forms.CharField(
        widget=forms.HiddenInput()
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control input-sm'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control input-sm'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control input-sm'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control input-sm"}),
        required=False,
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control input-sm"}),

        required=False,
    )

    sort = forms.CharField(
        widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}),
        initial=999,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 生成选择列表
        self.fields["menu_id"].choices += models.Menu.objects.values_list('id', 'title')
        # 当pid为空 menu不为空时  表示可以做菜单的选择项
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')
        self.fields['sort'].widget.attrs['value'] = '999'  # 初始化值
