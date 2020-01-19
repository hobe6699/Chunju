#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/17 9:01
# @Author  : mark.hu
# @Site    : 
# @File    : area.py
# @Software: PyCharm
# @Email:5898387@qq.com
from webapp import models
from django import forms


class AreaClassModelForm(forms.ModelForm):
    class Meta:
        model = models.msafety.AreaClass
        fields = ['name']
        # widgets = {'name': forms.TextInput(),
        #            'create_date': forms.DateTimeInput()}

    def __init__(self, *args, **kwargs):
        super(AreaClassModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm 字段添加样式
        for name, field in self.fields.items():  # name 字段名称  field字段本身
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'


class AreaModelForm(forms.ModelForm):
    class Meta:
        model = models.msafety.Area
        fields = ['name', 'barcode', 'emp', 'area_class']

    def __init__(self, *args, **kwargs):
        super(AreaModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm 字段添加样式
        for name, field in self.fields.items():  # name 字段名称  field字段本身
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'
        # 设置 barcode 为只读
        self.fields['barcode'].widget.attrs['readonly'] = True
