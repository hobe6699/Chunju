#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:23
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.shortcuts import render, HttpResponse, redirect
from django.urls import path, include, re_path, reverse
from django.utils.safestring import mark_safe
from types import FunctionType
from stark.utils import pagination
from django.http import QueryDict  # http请求数据
from django import forms
import functools
from stark.utils.get_custom_choice import get_choice_index, get_choice_list
from django.db.models import ForeignKey, CharField, IntegerField, ManyToManyField
from django.forms.fields import ImageField, DateTimeField, CharField, IntegerField, ChoiceField  # 用于判断前端控件类型


class SearchGroupRow(object):
    def __init__(self, title, queryset_or_tuple, search_option, request):
        """
        :param title: 组合搜索前面显示的标题
        :param queryset_or_tuple: 组合搜索关联到的数据
        :param search_option: 组合搜索配置
        """
        self.title = title
        self.queryset_or_tuple = queryset_or_tuple
        self.search_option = search_option
        self.request = request

    def __iter__(self):
        """
        __iter__可迭代方法
        对获取到的数据创建一个可迭代方法 并使用生成器生成想要的数据，生成器是一种特殊的迭代器
        :return:
        """
        yield "<tr>"
        yield "<td style='width:60px' class='text-center'>"
        yield "<h5  style='color:#4CA48B;'>%s:</h5>" % self.title
        yield "</td>"
        yield "<td style='margin: 1px;'>"
        total_query_dict = self.request.GET.copy()
        total_query_dict._mutable = True
        origin_value_list = self.request.GET.getlist(self.search_option.field)
        if not origin_value_list:
            yield "<a href='?%s'  style='margin: 1px;' class='btn btn-primary btn-outline btn-xs active'>全部</a>" % total_query_dict.urlencode()  # 对应返回不同的标签
        else:
            total_query_dict.pop(self.search_option.field)
            yield "<a href='?%s'  style='margin: 1px;' class='btn btn-primary btn-outline btn-xs'>全部</a>" % total_query_dict.urlencode()  # 对应返回不同的标签
        for item in self.queryset_or_tuple:  # 先获取每一个对象
            text = self.search_option.get_text(item)  # 获取要显示的文本
            value = self.search_option.get_value(item)  # 获取要显示的文本对应的值
            query_dict = self.request.GET.copy()  # 获取请求数据，并复制一份出来
            query_dict._mutable = True  # 将数据设为可编辑
            if not self.search_option.is_multi:
                query_dict[self.search_option.field] = value  # 请将求数据中对应参数的值 设为要显示的文本对应的值
                if str(value) in origin_value_list:  # 如果要当值 与请求的值一致，将前端标签 加的active属性。表示选中
                    query_dict.pop(self.search_option.field)
                    yield "<a href='?%s' style='margin: 1px;' class='btn btn-primary btn-outline btn-xs active'>%s</a>" % (
                        query_dict.urlencode(), text)  # 对应返回不同的标签
                else:
                    yield "<a href='?%s' style='margin: 1px;' class='btn btn-primary btn-outline btn-xs'>%s</a>" % (
                        query_dict.urlencode(), text)  # 对应返回不同的标签
            else:
                multi_value_list = query_dict.getlist(self.search_option.field)
                if str(value) in multi_value_list:
                    multi_value_list.remove(str(value))
                    query_dict.setlist(self.search_option.field, multi_value_list)
                    yield "<a href='?%s' style='margin: 1px;' class='btn btn-primary btn-outline btn-xs active'>%s</a>" % (
                        query_dict.urlencode(), text)  # 对应返回不同的标签

                else:
                    multi_value_list.append(str(value))
                    query_dict.setlist(self.search_option.field, multi_value_list)
                    yield "<a href='?%s' style='margin: 1px;' class='btn btn-primary btn-outline btn-xs'>%s</a>" % (
                        query_dict.urlencode(), text)  # 对应返回不同的标签

        yield "</td>"
        yield "</tr>"


class SearchOption(object):
    def __init__(self, field, db_condition=None, text_func=None, value_func=None, is_multi=True):
        """
        快速筛选 组合搜索配置
        :param field: 组合搜索关联字段
        :param db_condition: 数据库关联查询时的条件
        :param text_func: 用于自定义页面上标签显示的文本
        :param value_func: 用于自定义页面上标签的值
        :param is_multi: 用于定义快速筛选中的条件，是否支持多选
        """
        self.field = field
        if not db_condition:  # 没有传条件时，将条件置为空
            db_condition = {}
        self.db_condition = db_condition

        self.is_choice = False  # 用于判断是否是choice对象

        self.text_func = text_func
        self.value_func = value_func
        self.is_multi = is_multi

    def get_db_condition(self, request, *args, **kwargs):
        """
        # FK和M2M,关联表中的数据的查询条件，在这里写方法的原因是方便以后重构
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.db_condition

    def get_queryset_or_tuple(self, model_class, request, *args, **kwargs):
        """
        根据字段去数据库中获取关联的数据
        :return:
        """
        # 在自己对应的model类中找到字段对象
        field_object = model_class._meta.get_field(self.field)
        title = field_object.verbose_name
        # 获取数据
        if isinstance(field_object, ForeignKey) or isinstance(field_object, ManyToManyField):
            # FK和M2M,应该去获取关联表中的数据
            db_condition = self.get_db_condition(request, *args, **kwargs)
            return SearchGroupRow(title, field_object.related_model.objects.filter(**db_condition), self, request)
        else:
            # 获取choice中的数据
            self.is_choice = True
            return SearchGroupRow(title, field_object.choices, self, request)

    def get_text(self, field_object):
        """
        获取文本函数
        :param field_object: 字段对象
        :return:
        """
        if isinstance(self.text_func, FunctionType) and self.text_func:  # 是否有自定义的文显示函数
            return self.text_func(field_object)  # 有就返回自定义的
        if self.is_choice:  # 如果没有自定义的，先判断是不是元组，是返回元组的value
            return field_object[1]
        return str(field_object)  # 不是元组，返回对象str

    def get_value(self, field_object):
        """
        获取文本函数
        :param field_object: 字段对象
        :return:
        """
        if isinstance(self.value_func, FunctionType) and self.value_func:  # 是否有自定义的文显示函数
            return self.value_func(field_object)  # 有就返回自定义的
        if self.is_choice:  # 如果没有自定义的，先判断是不是元组，是返回元组的value
            return field_object[0]
        return str(field_object.pk)  # 不是元组，返回对象str


class TableHeaderUrl(object):
    def __init__(self, request, start_handler, verbose_name):
        """
        生成表的列表题，主要是处理标题上的a标签，给不同的标签赋于不同的功能
        比如 第一列的全选功能
        其它列的排序功能
        :param request: 请求信息
        :param start_handler: StartHandler类
        :param verbose_name: 表的列标题
        """
        self.request = request
        self.verbose_name = verbose_name
        self.name = "%s:%s" % (start_handler.site.namespace, start_handler.get_list_url_name)  # 获取list的url

    @property
    def get_header_url(self):
        verbose_name = self.verbose_name
        base_url = reverse(self.name)

        if self.request.GET:
            params = self.request.GET.copy()  # 获取GET的参数
            params._mutable = True  # 将参数允许编辑
            # if 'checkbox_selected_all' in verbose_name:
            #     if 'true' in params['checkbox_all']:
            #         params['checkbox_all'] = 'false'
            #         flag = False
            #     else:
            #         params['checkbox_all'] = 'true'
            #         flag = True
            # else:
            #     if '-' != params['verbose_name'][0:1]:
            #         params['verbose_name'] = "-%s" % verbose_name  # 0.2.3 给verbose_name添加一个负号，用来判断是正序还是反序
            #     else:
            #         params['verbose_name'] = verbose_name

            if params:
                if 'checkbox_selected_all' in verbose_name:
                    if 'checkbox_all' in params:
                        if 'true' in params['checkbox_all']:
                            params['checkbox_all'] = 'false'
                            flag = False
                        else:
                            params['checkbox_all'] = 'true'
                            flag = True
                        url = self.get_checkbox_all(params=params.urlencode(), flag=flag)
                    else:
                        params['checkbox_all'] = 'true'
                        flag = True
                        url = self.get_checkbox_all(params=params.urlencode(), flag=flag)
                    return url
                else:
                    print(params)
                    if 'verbose_name' in params:
                        if '-' != params['verbose_name'][0:1]:
                            params['verbose_name'] = "-%s" % verbose_name  # 0.2.3 给verbose_name添加一个负号，用来判断是正序还是反序
                        else:
                            params['verbose_name'] = verbose_name
                    else:
                        params['verbose_name'] = verbose_name
                    url = "<a href=%s?%s>%s</a>" % (base_url, params.urlencode(), verbose_name)  # 0.2.4、拼接url
                return url
            else:
                url = "%s?verbose_name=%s" % (base_url, verbose_name)
                url = '<a href=%s>%s</a>' % (url, verbose_name)
                return url

        else:
            if 'checkbox_selected_all' in verbose_name:  # 有一列作全选用，这里要处理一下
                # url = "%s?checkbox_all=%s'" % (base_url, verbose_name)
                url = self.get_checkbox_all()

            else:
                url = "%s?verbose_name=%s" % (base_url, verbose_name)
                url = '<a href=%s>%s</a>' % (url, verbose_name)
            return url

    def get_checkbox_all(self, params=None, flag=False):
        print(flag)
        if params:
            if flag:
                url = "<input type='checkbox'  onclick=\"location='?%s\'\">" % params
            else:
                url = "<input type='checkbox' checked onclick=\"location='?%s\'\">" % params
        else:
            url = "<input type='checkbox' onclick=\"location='?checkbox_all=%s\'\">" % 'true'
        return url


class DateTimePickerInput(forms.TextInput):
    template_name = 'stark/forms/widget/datetime_picker.html'


# 用于给控件添加样式
class StarkModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StarkModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, CharField) or isinstance(field, ChoiceField):
                field.widget.attrs['class'] = 'form-control input-sm'
                field.widget.attrs['autocomplete'] = 'off'


# 用于给控件添加样式
class StarkForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(StarkForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field, ImageField):
                field.widget.attrs['class'] = 'form-control input-sm'
                field.widget.attrs['autocomplete'] = 'off'


class StartHandler(object):
    """
    生成默认的url 和默认视图
    """

    def __init__(self, site, model_class, prev):
        """
        初始化时获取参数
        :param site: StarkSite类  用于后面获取当前url的namespace
        :param model_class: model模型
        :param prev: 用于区别相同模型，使用不同的url路径的前缀
        """
        self.model_class = model_class
        self.prev = prev
        self.site = site
        self.request = None  # 用于获取每次的请求信息

    list_display = []  # 用于定义列表显示的列
    per_page_count = 10  # 列表中每页显示的行数
    has_add_btn = True  # 用于判断是否有添加按钮
    model_form_class = None  # 用于用户自定制页面
    has_search = False  # 用于是否有搜索功能
    search_group = []  # 用于定义快速筛选的字段

    action_dict = {}  # 存放批量操作的函数
    list_template = None  # 用于自定义的列表页面的显示模版
    add_template = None  # 用于自定义的添加页面的显示模版
    edit_template = None  # 用于自定义的编码页面的显示模版
    delete_template = None  # 用于自定义的删除页面的显示模版

    def action_multi_delete(self, request, *args, **kwargs):
        """
        批量删除
        :param request: request请求，作用：将要删除的pk传进来
        :return:
        """
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
        name = "%s:%s" % (self.site.namespace, self.get_list_url_name)  # 获取list的url
        base_url = reverse(name)
        return redirect(base_url)

    def get_search_group(self):
        """
        为快速筛选保留的勾子函数
        :return:
        """
        return self.search_group

    def get_search_group_condition(self, request):
        """
        获取组合搜索的条件
        :param request:  请求
        :return:
        """
        condition = {}
        for option in self.get_search_group():  # 获取所有配置了搜索的字段
            if option.is_multi:  # 是否多选
                value_list = request.GET.getlist(option.field)  # 看一下 对应的字段，是否在请求中  getlist按列表方式获取请求的数据
                if not value_list:  # 不在，跳过继续下一次循环
                    continue
                else:  # 在拼接成查询条件
                    condition["%s__in" % option.field] = value_list
            else:  # 不是多选，单选的
                value = request.GET.get(option.field)  # 同样获取字段是否在请求中
                if not value:  # 不在跳过继续下一次循环
                    continue
                condition[option.field] = value  # 在拼接成查询条件 直接用字段 = 值

        return condition

    def get_action_dict(self):
        return self.action_dict

    def get_add_btn(self, request, *args, **kwargs):
        if self.has_add_btn:
            return "<a href='%s' class='btn btn-primary btn-sm'><i class='fa fa-plus'></i> 新增</a>" % self.revers_url(
                self.get_add_url_name, *args, **kwargs)
        return None

    def get_list_display(self):
        """
        获取页面上应该显示的列，预留的钩子函数，方便以后角色权限不同的显示不同列
        :return:
        """
        value = []
        if self.list_display:  # 当定义了显示名称时
            value.extend(self.list_display)  # 按显示名称显示，
            value.append(StartHandler.display_edit)  # 并默认加上编辑和删除方法
            value.append(StartHandler.display_del)

        return value

    def get_model_form_class(self, is_add, request, pk=None, *args, **kwargs):

        if self.model_form_class:  # 如果用户自定义一form页面，就使用用户自定义的
            return self.model_form_class

        class DynamicModelForm(StarkModelForm):
            class Meta:
                model = self.model_class
                fields = "__all__"

        return DynamicModelForm

    def display_edit(self, obj=None, is_header=None, *args, **kwargs):
        """
         自定义在列表中显示的列
        :param obj: 表体显示的内空
        :param is_header:  表头标题
        :return:
        """
        if is_header:
            return "编辑"
        if obj:
            # name = "%s:%s" % (self.site.namespace, self.get_change_url_name)
            # url = reverse(name, args=(obj.pk,))
            url = self.revers_url(self.get_change_url_name, pk=obj.pk)
            return mark_safe("<a href='%s'><i class='fa fa-edit fa-lg' style='color: #18A689'></i></a>" % url)

    def display_del(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return "删除"
        if obj:
            url = self.revers_url(self.get_delete_url_name, pk=obj.pk)
            return mark_safe("<a href='%s'><i class='fa fa-trash fa-lg' style='color: #CC6666'></i></a>" % url)

    def display_id(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return 'ID'
        if obj:
            return mark_safe("%s" % obj.pk)

    def display_checkbox(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return 'checkbox_selected_all'
        if obj:
            return mark_safe("<input type='checkbox' name='pk' value=%s>" % obj.pk)

    def list_view(self, request, *args, **kwargs):

        action_dict = self.get_action_dict()  # 获取批量操作的功能列表
        # 批量操作处理
        if request.method == 'POST':
            action_func_name = request.POST.get('action')  # 1、获取方法名
            if action_func_name and action_func_name in action_dict:  # 2、 检查方法是否在定义的方法列表中
                func = getattr(self, action_func_name)  # 3、反射 获取到对应的方法
                action_response = func(request, *args, **kwargs)  # 4、执行方法
                if action_response:  # 5、方法是否有返回值
                    return action_response  # 6、有返回值就传递到前端

        list_display = self.get_list_display()
        # 0、处理表格的表头
        header_list = []  # 表头的标题
        if list_display:
            for key_or_func in list_display:
                # 0.1、遍历 要显示的列名称，根据列名称获取 models中定义的verbose_name列名
                if isinstance(key_or_func, FunctionType):  # 判断是否是函数
                    verbose_name = key_or_func(self, obj=None, is_header=True)
                else:
                    verbose_name = self.model_class._meta.get_field(key_or_func).verbose_name
                # 0.2、给表头增加排序功能
                url = TableHeaderUrl(request, self, verbose_name).get_header_url
                header_list.append(url)
        else:  # 如果没定义 要显示的列，就显示model的名称
            header_list.append(self.model_class._meta.model_name)
        #  处理表格的表体数据
        # 1、处理请求
        per_page_count = request.GET.get('per_page_count')  # 每页显示的行数
        verbose_name = request.GET.get('verbose_name')  # 请求排序字段的名称
        # 1.1 排序处理

        sort_field = []  # 获取排序的字段
        if verbose_name:
            for field in self.model_class._meta.fields:
                if '-' == verbose_name[0:1]:
                    if field.verbose_name == verbose_name[1:]:
                        sort_field.append("-%s" % field.name)
                else:
                    if field.verbose_name == verbose_name:
                        sort_field.append(field.name)

        # 1.2 全局搜索处理

        from django.db.models import Q  # Q 用于构造复杂的查询条件
        search_context = request.POST.get('search_context', '')
        conn = Q()  # Q查询
        conn.connector = 'OR'  # 多个字段用OR连接
        # 拼接查询条件
        if self.has_search:  # 是否有搜索功能
            if search_context:  # 是否有搜索请求
                for field in self.model_class._meta.fields:  # 遍历每一个model中的字段，获取字类型后，拼装搜索条件
                    if isinstance(field, ForeignKey):
                        conn.children.append(("%s__name__contains" % field.name, search_context))

                    if isinstance(field, IntegerField):
                        if field.name != 'ID':
                            t = get_choice_list(self.model_class, field.name)
                            if t:
                                for item in t:
                                    if search_context in item[1]:
                                        conn.children.append(("%s" % field.name, item[0]))
                    if isinstance(field, CharField):
                        conn.children.append(("%s__contains" % field.name, search_context))
        # 1.3组合搜索处理
        search_group_condition = self.get_search_group_condition(request)

        # from webcore.models.organization import OrgEmp
        # q = OrgEmp.objects.filter()

        # 2、分页处理

        queryset = self.model_class.objects.filter(conn).filter(**search_group_condition).order_by(*sort_field)  # 获取数据

        all_count = queryset.count()  # 获取总数
        query_params = request.GET.copy()
        query_params._mutable = True

        if per_page_count:
            per_page = int(per_page_count)  # 当前端定义分页时，使用前端定义的
        else:
            per_page = self.per_page_count  # 没定义时，使用默认的

        # 2.1 处理分页控件
        pager = pagination.Pagination(
            current_page=request.GET.get('page'),
            all_count=all_count,
            base_url=request.path_info,
            query_params=query_params,
            per_page=per_page,
        )

        data_list = queryset[pager.start:pager.end]  # 获取分页数据
        body_list = []
        for row in data_list:  # 遍历数据，按list_display显示每一行的数据
            row_list = []
            if list_display:
                for key_or_func in list_display:
                    if isinstance(key_or_func, FunctionType):
                        row_list.append(key_or_func(self, row, is_header=False))

                    else:
                        row_list.append(getattr(row, key_or_func))  # getattr功能 按 字段名称获取行中对应的数据
            else:  # 如果没有list_display 就显示默认的行数据
                row_list.append(row)
            body_list.append(row_list)

        # 处理全选事件
        checkbox_all = request.GET.get('checkbox_all')
        if checkbox_all:
            if 'true' in checkbox_all:
                row_list = []
                for row in body_list:
                    # 将字符串转为列表
                    str_list = list(row[0])
                    # 找到位置
                    nPos = str(row[0]).index('>')

                    str_list.insert(nPos, ' checked')

                    new_str = "".join(str_list)
                    row.pop(0)
                    row.insert(0, mark_safe(new_str))
                    row_list.append(row)
                body_list.clear()
                body_list = row_list

        # 快速筛选--组合搜索
        search_group = self.get_search_group()
        search_row_list = []
        for item in search_group:
            # 在自己对应的model类中找到字段对象
            row = item.get_queryset_or_tuple(self.model_class, request, *args, **kwargs)
            search_row_list.append(row)

        return render(request,
                      self.list_template or 'stark/list.html',  # self.list_template or 'stark/list.html'使用自定义的模版没有就用默认的
                      {
                          "header_list": header_list,  # 表头数据
                          "body_list": body_list,  # 表体数据
                          "pager": pager,  # 显示当前是第几页
                          "start": pager.start + 1,  # 显示当前页面开始的条数
                          "end": pager.end if pager.end < pager.all_count else pager.all_count,  # 显示目前页面是第几条
                          'add_btn': self.get_add_btn(request, *args, **kwargs),  # 添加按钮
                          'has_search': self.has_search,  # 定义是否有搜索功能
                          'search_context': search_context,  # 搜索框内容
                          'action_dict': action_dict,  # 执行事件列表
                          'search_group': search_group,  # 快速筛选
                          'search_row_list': search_row_list,  # 快速筛选的数据
                      }
                      )

    def save(self, request, form, is_update, *args, **kwargs):
        """
        将保存动作分离出来后，方便用户自定制保存时的动作，比如给某个字段设置默认值
        :param form: 表单
        :param is_update:
        :return:
        """
        form.save()

    def add_view(self, request, *args, **kwargs):
        model_form_class = self.get_model_form_class(True, request=request, *args, **kwargs)
        url = self.reverse_list_url(*args, **kwargs)
        if request.method == "GET":
            form = model_form_class()
            return render(request, self.add_template or 'stark/change.html', {"form": form, 'cancel': url})

        form = model_form_class(data=request.POST)
        if form.is_valid():
            response = self.save(request, form, False, *args, **kwargs)
            # 保存成功后，返回列表页面
            return response or redirect(url)
        return render(request, self.add_template or 'stark/change.html', {"form": form, 'cancel': url})

    def get_change_object(self, request, pk, *args, **kwargs):
        return self.model_class.objects.filter(pk=pk).first()

    def change_view(self, request, pk, *args, **kwargs):
        url = self.reverse_list_url(*args, **kwargs)

        current_change_object = self.get_change_object(request, pk, *args, **kwargs)  # 数据是否存在
        if not current_change_object:
            return HttpResponse('要修改的数据不存在!，请重新选择')  # 如果不存在，返回错误信息

        model_form_class = self.get_model_form_class(False, request, pk, *args, **kwargs)

        if request.method == "GET":
            form = model_form_class(instance=current_change_object)
            return render(request, self.edit_template or 'stark/change.html', {"form": form, 'cancel': url})

        form = model_form_class(data=request.POST, instance=current_change_object)

        if form.is_valid():
            response = self.save(request, form, True, *args, **kwargs)
            # 保存成功后，返回列表页面
            return response or redirect(url)
        return render(request, self.edit_template or 'stark/change.html', {"form": form, 'cancel': url})

    def delete_object(self, request, pk, *args, **kwargs):
        return self.model_class.objects.filter(pk=pk).delete()

    def delete_view(self, request, pk, *args, **kwargs):
        url = self.reverse_list_url(*args, **kwargs)
        if request.method == "GET":
            return render(request, self.delete_template or 'stark/delete.html/', {'pk': pk, "cancel": url})
        response = self.delete_object(request, pk, *args, **kwargs)
        return response or redirect(url)  # 跳转回列表页面

    def get_url_name(self, param):
        """
        生成url的名称
        :param param: url的类型 如 list、add....
        :return: 返回生成的url
        """
        # 获取app名称 model名称用于拼接url
        app_label, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name

        # 是否存在用于区别模型的前缀
        if self.prev:
            return '%s_%s_%s_%s' % (app_label, model_name, self.prev, param)
        return '%s_%s_%s' % (app_label, model_name, param)

    @property
    def get_list_url_name(self):
        """
        :return: 生成 list列表url名称
        """
        return self.get_url_name('list')

    @property
    def get_add_url_name(self):
        """
        :return: 生成 添加 url名称
        """
        return self.get_url_name('add')

    @property
    def get_change_url_name(self):
        """
        :return: 生成编辑url名称
        """
        return self.get_url_name('change')

    @property  # 将方法以属性的方式表示
    def get_delete_url_name(self):
        """
        :return: 生成删除url名称
        """
        return self.get_url_name('delete')

    def revers_url(self, name, *args, **kwargs):
        """
        反向生成  url 主要目的保留原url的参数
        :param name:  要生成url类型  新增 修改 删除
        :param pk:  如果是 修改 或删除，需要把ID传过来
        :return: 反回一个新的url
        """

        name = "%s:%s" % (self.site.namespace, name)
        base_url = reverse(name, args=args, kwargs=kwargs)
        if not self.request.GET:
            url = base_url
        else:  # 如果有请求信息  作用保留原链接中的参数，当新增完成后，按原参数进行加载页面。保持原页面状态
            param = self.request.GET.urlencode()  # 1、获取请求中的参数
            new_query_dict = QueryDict(mutable=True)  # 2、实例化一个新的参数
            new_query_dict["_filter"] = param  # 3、将请求的所有参数打包 赋给新的参数 _filter
            url = "%s?%s" % (base_url, new_query_dict.urlencode())  # 4、拼接url

        return url

    def reverse_list_url(self, *args, **kwargs):
        """
        按带有_filter参数值返回原地址
        :return:
        """
        name = "%s:%s" % (self.site.namespace, self.get_list_url_name)
        base_url = reverse(name, args=args, kwargs=kwargs)
        param = self.request.GET.get('_filter')
        if not param:  # 如果没参数  直拉返回原地址
            url = base_url
        else:
            url = "%s?%s" % (base_url, param)  # 如果有，拼接地址和原参数
        return url

    def wrapper(self, func):
        """
        装饰器：用于截获取请求时的数据。
        :param func:
        :return:
        """

        @functools.wraps(func)  # 作用，保留原函数的原始信息
        def inner(request, *args, **kwargs):
            self.request = request  # 将请求request赋值给变量self.request 方便其它方法中调用
            return func(request, *args, **kwargs)

        return inner

    def get_urls(self):
        """
        :return:  默认生成4个常规的路由
        """

        patterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            # name='%s_%s_list' 设置url的别名
            re_path(r'^add/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r'^change/(?P<pk>\d+)/$', self.wrapper(self.change_view), name=self.get_change_url_name),
            re_path(r'^delete/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        patterns.extend(self.extra_urls())  # 添加额外的路由
        return patterns

    def extra_urls(self):
        """
        :return: 用于增加额外的路由
        """
        return []


class StarkSite(object):
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class=None, prev=None):
        """

        :param model_class: 是models中数据库相关的类
        :param handler_class: 是models中数据表的视图对象 相当于views
        :param prev: 生成url的前缀
        :return:
        """
        if not handler_class:  # 如果没有定义视图函数 ，就用默认的
            handler_class = StartHandler

        self._registry.append(
            {'model_class': model_class, 'handler': handler_class(self, model_class, prev),
             'prev': prev})  # 把model注册进来的目的，是对对应的表做增册改查

    def get_urls(self):  # 生成url
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']  # 不同models生成的views
            prev = item['prev']
            app_label, model_name = model_class._meta.app_label, model_class._meta.model_name
            if prev:
                patterns.append(
                    re_path(r'^%s/%s/%s/' % (app_label, model_name, prev), (handler.get_urls(), None, None)))

            else:
                patterns.append(re_path(r'^%s/%s/' % (app_label, model_name), (handler.get_urls(), None, None)))

        return patterns

    @property  # 将方法用属性的方式表示
    def urls(self):

        return self.get_urls(), self.app_name, self.namespace


site = StarkSite()
