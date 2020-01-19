#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/9 17:34
# @Author  : mark.hu
# @Site    : 
# @File    : organization.py
# @Software: PyCharm
# @Emial:5898387@qq.com

from django.template import (
    Library,
)

register = Library()


@register.inclusion_tag('organization/person.html')
def person(request):
    emp = request.session.get('emp')
    return {'emp': emp}
