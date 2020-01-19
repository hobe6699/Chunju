#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 16:29
# @Author  : mark.hu
# @Site    : 
# @File    : organization.py
# @Software: PyCharm
# @Emial:5898387@qq.com
from django.db import models


# 集团信息
class OrgGroup(models.Model):
    name = models.CharField(verbose_name="组织名称", max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'org_group'


# 组织信息
class OrgInfo(models.Model):
    org_group = models.ForeignKey(to='OrgGroup', on_delete=models.CASCADE, verbose_name="所属组织", null=True, blank=True)
    name = models.CharField(max_length=512, verbose_name="单位名称")
    full_name = models.CharField(max_length=512, verbose_name="单位全称")
    img = models.ImageField(upload_to='sys', verbose_name="图标")
    address = models.CharField(max_length=1024, verbose_name="地址", null=True, blank=True)
    telephone = models.CharField(max_length=32, verbose_name="电话", null=True, blank=True)
    zip = models.CharField(max_length=16, verbose_name="邮编", null=True, blank=True)
    website = models.CharField(max_length=512, verbose_name="公司网站", null=True, blank=True, default='#')
    create_date = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'org_info'

    # 在models中新建一个函数，用来判断自身的img字段是否为空，不为空则返回self.img.url
    @property
    def img_url(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url


# 部门信息
class OrgDept(models.Model):
    org_info = models.ForeignKey(to='OrgInfo', on_delete=models.CASCADE, verbose_name="所属单位")
    parent = models.ForeignKey(to='OrgDept', on_delete=models.CASCADE, verbose_name="上级部门", null=True, blank=True)
    name = models.CharField(max_length=512, verbose_name="部门名称")
    create_date = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'org_dept'


# 岗位信息
class OrgPosition(models.Model):
    org_info = models.ForeignKey(to='OrgInfo', on_delete=models.CASCADE, verbose_name="所属单位")
    org_dept = models.ForeignKey(to='OrgDept', on_delete=models.CASCADE, verbose_name="所属部门")
    parent = models.ForeignKey(to='OrgPosition', on_delete=models.CASCADE, verbose_name="上级岗位", null=True, blank=True)
    name = models.CharField(max_length=512, verbose_name="岗位名称")
    create_date = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'org_position'


class OrgEmp(models.Model):
    org_info = models.ForeignKey(to='OrgInfo', on_delete=models.CASCADE, verbose_name="所属单位")
    org_dept = models.ForeignKey(to='OrgDept', on_delete=models.CASCADE, verbose_name="所属部门")
    org_position = models.ForeignKey(to='OrgPosition', on_delete=models.CASCADE, verbose_name="所属岗位")
    name = models.CharField(max_length=512, verbose_name="姓名")
    account = models.ForeignKey(to='rbac.UserInfo', on_delete=models.CASCADE, verbose_name="账号")
    img = models.ImageField(upload_to='sys', verbose_name="头像", default="person.png", null=True, blank=True)
    create_date = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    wechat = models.CharField(max_length=128, verbose_name="微信号", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'org_emp'
        app_label = 'webcore'
