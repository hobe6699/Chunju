#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 17:21
# @Author  : mark.hu
# @Site    : 
# @File    : role.py
# @Software: PyCharm
# @Email:5898387@qq.com
from webcore.models import organization
from django import forms


class OrgGroupModelForm(forms.ModelForm):
    class Meta:
        model = organization.OrgGroup
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        }
