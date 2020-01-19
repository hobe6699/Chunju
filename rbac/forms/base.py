#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/17 11:59
# @Author  : mark.hu
# @Site    : 
# @File    : base.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django import forms


# 用于给控件添加样式
class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootStrapModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'
