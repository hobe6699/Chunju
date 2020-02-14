#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:23
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.shortcuts import render, redirect, HttpResponse
from django.core.serializers import serialize
import json
from contract.models.signature import ContractUser


def auth(request):
    if request.method == "GET":
        return render(request, 'auth.html')
    username = request.POST.get('username')
    code = request.POST.get('code')
    current_user = ContractUser.objects.filter(username=username, code=code).first()
    if not current_user:
        obj = ContractUser.objects.filter(code=code).first()
        if obj:
            return render(request, 'auth.html', {"msg": "工号已存在，或工号与姓名不一致"})
        ContractUser.objects.create(username=username, code=code)
    current_user = ContractUser.objects.filter(username=username, code=code).first()
    emp = {'pk': current_user.pk,
           'username': current_user.username,
           'code': current_user.code,
           'department': current_user.department,

           }
    request.session['emp'] = emp
    request.session['title'] = '苏州热工研究院有限公司'
    return redirect('/contract/contract_context/')


def code(request):
    username = request.POST.get('username')
    if len(username) > 1 and username != ' ':
        obj = ContractUser.objects.filter(username__contains=username).values('code')
        if obj:
            data = []
            for item in obj:
                data.append(item['code'])
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse('9')
    return HttpResponse(0)
