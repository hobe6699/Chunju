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
from django.core.exceptions import ValidationError  # 验证结果的错误信息


class UserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码')  # 在表单上创建额外的字段
    # 给字段添加样式
    confirm_password.widget_attrs(
        forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', 'password', 'confirm_password']

        # 设置错误信息
        error_messages = {
            'name': {'required': "用户名不能为空"}
        }

    # 初始化方法
    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm 字段添加样式
        for name, field in self.fields.items():  # name 字段名称  field字段本身
            if 'password' in name:
                field.widget = forms.PasswordInput()
            if 'mail' in name:
                field.widget = forms.EmailInput()
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'

    # 做额外的校验   勾子方法
    def clean_confirm_password(self):
        """
        验证两次密码是否一致
        :return:
        """
        password = self.cleaned_data['password']  # 获取提交的密码
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:  # 如果密码不一致  返回错误信息
            raise ValidationError('确认密码不一致!')
        return confirm_password


class UpdateUserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'email']

        # 设置错误信息
        error_messages = {
            'name': {'required': "用户名不能为空"}
        }

    # 初始化方法
    def __init__(self, *args, **kwargs):
        super(UpdateUserModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm 字段添加样式
        for name, field in self.fields.items():  # name 字段名称  field字段本身
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'


class ResetPasswordUserModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码')  # 在表单上创建额外的字段
    # 给字段添加样式
    confirm_password.widget_attrs(
        forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']

    # 初始化方法
    def __init__(self, *args, **kwargs):
        super(ResetPasswordUserModelForm, self).__init__(*args, **kwargs)
        # 统一给ModelForm 字段添加样式
        for name, field in self.fields.items():  # name 字段名称  field字段本身
            if 'password' in name:
                field.widget = forms.PasswordInput()
            if 'mail' in name:
                field.widget = forms.EmailInput()
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['autocomplete'] = 'off'

    # 做额外的校验   勾子方法
    def clean_confirm_password(self):
        """
        验证两次密码是否一致
        :return:
        """
        password = self.cleaned_data['password']  # 获取提交的密码
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:  # 如果密码不一致  返回错误信息
            raise ValidationError('确认密码不一致!')
        return confirm_password
