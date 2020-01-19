#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/10 11:34
# @Author  : mark.hu
# @Site    : 
# @File    : ent_wachat_verify.py
# @Software: PyCharm
# @Emial:5898387@qq.com
from django.shortcuts import render


def ent_wachat_verify(request):
    print(request)
    if request.method == 'GET':
        return render(request, 'WW_verify_83z6GYOPGCfBqcDy.txt')
