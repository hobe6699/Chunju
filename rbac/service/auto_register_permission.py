#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 14:45
# @Author  : mark.hu
# @Site    : 
# @File    : auto_register_permission.py
# @Software: PyCharm
# @Email:5898387@qq.com
from rbac.service import routes
from rbac.models import Menu, Permission, Role
from django.core.serializers import serialize
import json
from django.db.models import Q


class AutoRegisterPermission(object):
    def __init__(self, select_str, menu_name, table_name, table_title):
        self.menu_list = dict()
        self.menu_list["select_str"] = select_str
        self.menu_list["menu_name"] = menu_name
        self.menu_list["table_name"] = table_name
        self.menu_list["table_title"] = table_title

    def init_permission(self):
        url = routes.get_all_url_dict()
        # self.get_permission_list(self,'org', '组织权限', 'orgemp', '人员')
        menu_list = self.menu_list
        select_str = menu_list["select_str"]
        menu_name = menu_list["menu_name"]
        table_name = menu_list["table_name"]
        table_title = menu_list["table_title"]
        for k, v in url.items():
            name = v['name']
            url = v['url']
            if select_str in str(k):
                menu_id = self.check_menu(menu_name)
                if table_name in str(k):
                    self.add_permission(name_class=table_name, name=name, url=url, menu_id=menu_id, title=table_title)

    def add_permission(self, name_class, name, url, menu_id, title):
        name = name
        url = url
        obj = Permission.objects.get(name=name)
        if obj:
            return

        if name_class in name and 'add' in name:
            pid = self.check_permission_is_menu(name_class, 'list')
            self.check_permission(name=name, url=url, title='%s_添加' % title, pid=pid)
        if name_class in name and 'change' in name or 'edit' in name:
            pid = self.check_permission_is_menu(name_class, 'list')
            self.check_permission(name=name, url=url, title='%s_编辑' % title, pid=pid)
        if name_class in name and 'delete' in name or 'del' in name:
            pid = self.check_permission_is_menu(name_class, 'list')
            self.check_permission(name=name, url=url, title='%s_删除' % title, pid=pid)
        if name_class in name and 'list' in name:
            self.check_permission(name=name, url=url, title='%s' % title, menu_id=menu_id)

    def check_menu(self, name):
        """
        检查一级菜单是否存在，存在返回pk ,不存在添加并返回pk
        :param name: 菜单标题
        :return: 对应的pk
        """
        obj = Menu.objects.filter(title=name).all()
        if not obj:
            Menu.objects.create(title=name, icon='fa-th')
            obj = Menu.objects.filter(title=name).all()
        menu = json.loads(serialize('json', obj))
        pk = menu[0]['pk']
        return pk

    def check_permission_is_menu(self, name, pams):
        """
        检查二级菜单是否存在
        :param pams1:名称
        :param pams2:类型
        :return:
        """

        obj = Permission.objects.filter(Q(name__contains=name) & Q(name__contains=pams))
        pk = None
        if obj:
            permission = json.loads(serialize('json', obj))
            pk = permission[0]['pk']
        return pk

    def check_permission(self, name, url, title, pid=None, menu_id=None):
        """
        创建权限
        :param name: 路径别名
        :param url: url
        :param title:标题
        :param pid: 父级id
        :param menu_id: 菜单ID
        :return: pk
        """
        if menu_id:
            obj = Permission.objects.filter(name=name)
            if not obj:
                Permission.objects.create(name=name, title=title, url=url, menu_id=menu_id)
                obj = Permission.objects.filter(name=name)
        else:
            obj = Permission.objects.filter(name=name)
            if not obj:
                Permission.objects.create(name=name, title=title, url=url, pid_id=pid)
                obj = Permission.objects.filter(name=name)
        if obj:
            p_obj = Permission.objects.get(name=name)
            self.check_system_admin(p_obj)
        return obj

    def check_system_admin(self, p_obj):
        """
        检查系统管理员是否存在
        :return: pk
        """
        obj = Role.objects.filter(title='admin')
        if not obj:
            Role.objects.create(title='admin')
        r_obj = Role.objects.get(title='admin')
        rp = Role.objects.filter(title='admin', permissions=p_obj).exists()
        if not rp:
            r_obj.permissions.add(p_obj)
