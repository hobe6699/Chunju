#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:23
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com
from stark.service.v1 import site
from contract.views.signature import SignatureHandler

site.register(SignatureHandler)
