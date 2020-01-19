#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 17:21
# @Author  : mark.hu
# @Site    : 
# @File    : role.py
# @Software: PyCharm
# @Email:5898387@qq.com
from rbac import models
from django import forms


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        }
