#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'mark'
__mtime__ = '2020-02-10'
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
from webcore.utils import md5
from django import forms
from django.core.exceptions import ValidationError  # 验证结果的错误信息
from django.utils.safestring import mark_safe
from django.urls import re_path
from django.shortcuts import render, redirect, HttpResponse
from webcore.models.organization import *
from stark.utils.get_custom_choice import get_choice_text, get_datetime_text
from stark.forms import widgets


class OrgGroupHandler(StartHandler):
    list_display = ['name', ]


class ImageForm(forms.Form):
    img = forms.ImageField(label='图片：')


class OrgInfoHandler(StartHandler):
    list_display = ['org_group', 'name', 'full_name', 'img', 'address', 'telephone',
                    get_datetime_text('创建时间', 'create_date')]

    def save(self, request, form, is_update, *args, **kwargs):
        # MyImageForm = ImageForm(request.FILES)
        # print(MyImageForm)
        # if MyImageForm.is_valid():
        #     print('ok')
        #     org_info = OrgInfo()
        #     org_info.img = MyImageForm.cleaned_data['picture']
        #     org_info.save()
        img = request.FILES.get('img')

        form.cleaned_data['img'] = img
        print(form.cleaned_data)
        form.save()


class OrgDeptHandler(StartHandler):
    list_display = ['org_info', 'parent', 'name']


class OrgPositionHandler(StartHandler):
    list_display = ['org_info', 'org_dept', 'parent', 'name']


class OrgEmpAddModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码')  # 在表单上创建额外的字段
    # 给字段添加样式
    confirm_password.widget_attrs(
        forms.TextInput(attrs={'type': 'password', 'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = OrgEmp
        fields = ['org_info', 'org_dept', 'org_position', 'username', 'name', 'email', 'hire_date', 'wechat',
                  'password',
                  'confirm_password',
                  'roles']

        # 设置错误信息
        error_messages = {
            'name': {'required': "用户名不能为空"}
        }

        widgets = {
            'hire_date': widgets.DateTimePickerInput
        }

    # 初始化方法
    def __init__(self, *args, **kwargs):
        super(OrgEmpAddModelForm, self).__init__(*args, **kwargs)
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
            raise ValidationError('两次密码不一致!')
        return confirm_password

    # 保存前对字段进行处理，这里是对密码进行加密
    def clean(self):
        password = self.cleaned_data['password']  # 获取提交的密码
        self.cleaned_data['password'] = md5.get_md5(password)  # 对密码进行加密
        return self.cleaned_data


class OrgEmpEditModelForm(StarkModelForm):
    class Meta:
        model = OrgEmp
        fields = ['org_info', 'org_dept', 'org_position', 'username', 'name', 'email',
                  'hire_date', 'wechat', 'roles']
        widgets = {
            'hire_date': widgets.DateTimePickerInput
        }


class OrgEmpResetPasswordForm(StarkForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)  # 在表单上创建额外的字段
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)  # 在表单上创建额外的字段

    class Meta:
        model = OrgEmp
        fields = ['password',
                  'confirm_password',
                  ]

    # 做额外的校验   勾子方法
    def clean_confirm_password(self):
        """
        验证两次密码是否一致
        :return:
        """
        password = self.cleaned_data['password']  # 获取提交的密码
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:  # 如果密码不一致  返回错误信息
            raise ValidationError('两次密码不一致!')
        return confirm_password

    # 保存前对字段进行处理，这里是对密码进行加密
    def clean(self):
        password = self.cleaned_data['password']  # 获取提交的密码
        print(password)
        self.cleaned_data['password'] = md5.get_md5(password)  # 对密码进行加密
        return self.cleaned_data


class OrgEmpHandler(StartHandler):
    def display_reset_password(self, obj=None, is_header=None, *args, **kwargs):
        """
        添加额外的字段 重置密码
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '重置密码'
        url = self.revers_url(self.get_reset_password_url_name, pk=obj.pk, *args, **kwargs)
        return mark_safe("<a href='%s'>重置密码</a>" % url)

    @property
    def get_reset_password_url_name(self):
        """
        生成url的别名
        :return:
        """
        return self.get_url_name('reset_pwd')

    def extra_urls(self):
        """
        添加额外的url 重置密码 的url
        :return:
        """
        patterns = [
            re_path(r'^reset/password/(?P<pk>\d+)/$', self.wrapper(self.reset_password),
                    name=self.get_reset_password_url_name),  # self.get_url_name('reset_pwd') 设置别名
        ]
        return patterns

    def reset_password(self, request, pk, *args, **kwargs):
        """
        为 重置密码添加 View 视图函数
        :param request:
        :param pk:
        :return:
        """
        current_object = self.get_change_object(request, pk, *args, **kwargs)  # 数据是否存在
        if not current_object:
            return HttpResponse('要修改的数据不存在!，请重新选择')  # 如果不存在，返回错误信息
        url = self.reverse_list_url()
        if request.method == 'GET':
            form = OrgEmpResetPasswordForm()
            return render(request, 'organization/reset_password.html', {'form': form, 'cancel': url})

        form = OrgEmpResetPasswordForm(data=request.POST)
        if form.is_valid():
            current_object.password = form.cleaned_data['password']
            current_object.save()
            return redirect(url)
        return render(request, 'organization/reset_password.html', {'form': form, 'cancel': url})

    list_display = [StartHandler.display_checkbox, StartHandler.display_id, 'org_info', 'org_dept', 'org_position',
                    'username', 'name', 'email',
                    get_choice_text('性别', 'gender'),
                    'wechat', display_reset_password]

    def get_model_form_class(self, is_add, request, pk=None, *args, **kwargs):  # 自定义modelform
        if is_add:  # 如果是添加，返回添加页面
            return OrgEmpAddModelForm
        return OrgEmpEditModelForm  # 否则返回修改页面

    has_search = True
    # search_list = ['org_info_name__contains', 'org_dept_name__contains', 'name__contains', 'org_dept_name__contains', ]
    action_dict = {'action_multi_delete': '批量删除'}

    # def get_list_display(self):
    #     return ['name', 'account',  StartHandler.display_edit,
    #                 StartHandler.display_del]
    search_group = [
        SearchOption('gender', is_multi=False),
        SearchOption('org_dept', {'id__gt': 0}),
        SearchOption('org_position', {'id__gt': 0}),
    ]
