#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/20 16:23
# @Author  : mark.hu
# @Site    : 
# @File    : stark.py
# @Software: PyCharm
# @Email:5898387@qq.com
from django.shortcuts import render, redirect, HttpResponse
from contract.models.signature import *
import datetime, json
from django.core.serializers import serialize


def signature(request):
    emp = request.session.get('emp')
    print(emp)
    title = request.session.get('title')
    date = datetime.datetime.now()
    if not emp:
        return redirect('/contract/auth/')
    pk = emp['pk']
    # sig_obj = Signature.objects.filter(name_id=pk).count()
    # if sig_obj:
    #     request.session['msg'] = '已经提交过了！'
    #     return redirect('/success/')
    if request.method == 'GET':
        return render(request, 'contract_context.html', {'emp': emp, 'date': date, 'title': title})
    sig = request.POST.get('sig')  # 获取签名
    sig_length = request.POST.get('sig_length')  # 获取签名长度
    if int(sig_length) <= 0:
        return render(request, 'contract_context.html', {'emp': emp, 'date': date, 'title': title, 'msg': '请签名!'})
    obj = Signature.objects.create(name_id=pk, signature=sig)
    if obj:
        request.session['msg'] = '提交完成!'
        return redirect('/success/')
    return render(request, 'contract_context.html', {'emp': emp, 'date': date, 'title': title})


def get_signature(request):
    pk_list = request.POST.get('pk_list')
    pl = json.loads(pk_list)

    data = Signature.objects.filter(id__in=pl).values("signature", 'create_date')
    sig_list = []
    for item in data:
        rs = {}
        rs['signature'] = item['signature']
        rs['create_date'] = str(item['create_date'].strftime('%Y-%m-%d %H:%m:%S'))
        sig_list.append(rs)
    return HttpResponse(json.dumps(sig_list))
