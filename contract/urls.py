#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:23
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com

from django.urls import path, re_path
from contract.views import auth, signature

app_name = 'contract'
urlpatterns = [
    re_path(r"^auth/$", auth.auth, name='contract_auth'),
    re_path(r"^code/$", auth.code, name='contract_code'),
    re_path(r"^contract_context/$", signature.signature, name='contract_signature'),
    re_path(r"^get_signature/$", signature.get_signature, name='contract_get_signature'),
]
