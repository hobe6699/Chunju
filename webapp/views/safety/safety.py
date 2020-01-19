#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-01-02 14:22
# @Author  : mark.hu
# @Site    : www.ivan.net.cn
# @File    : safety.py
# @Software: PyCharm
from django.shortcuts import render, HttpResponse, redirect
from webapp.models import *
import json
from webcore.models import organization
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def inspect(request):
    wechat_user_id = request.session.get('wechat_user_id')
    emp = request.session["emp"]
    if not emp:
        emp = organization.OrgEmp.objects.filter(wechat=wechat_user_id).values('pk', 'name', 'org_info',
                                                                               'org_info__name',
                                                                               'org_info__img', 'org_info__full_name',
                                                                               'org_info__website',
                                                                               'org_dept', 'org_dept__name',
                                                                               'org_position',
                                                                               'org_position__name', 'account',
                                                                               'account__name', 'account__email', 'img',
                                                                               'wechat').first()  # 获取人员信息

        request.session["emp"] = emp

    # client = wechat_signature.base_authorization.get_access_client()
    # client.message.send_text(agent_id=settings.APP_ID, user_ids='mark|wangw',content='主动发消息')
    # print(request.get_host())
    # url = "http://%s/webapp/inspect/" % request.get_host()
    # client.message.send_text_card(agent_id=settings.APP_ID, user_ids='mark', title="消息测试",
    #                description="<div class=\"gray\">2016年9月26日</div> <div class=\"normal\">恭喜你抽中iPhone 7一台， 领奖码：xxxx</div><div class=\"highlight\">请于2016年10月10日前联系行政同事领取</div>",
    #                url=url)
    from wechatpy.enterprise.client.api import menu
    # msg = client.menu.get(settings.APP_ID)

    # client.message.send_text(agent_id=settings.APP_ID, user_ids='mark', content=msg)
    # 获取用户ID
    # 获取检查的区域

    area_quest = msafety.Area.objects.filter(emp__wechat=wechat_user_id).values("id",
                                                                                "name", )  # msafety.Duty.objects.filter(ent_wx_code=wechat_user_id).values('id', 'area__id', 'area__name')
    area_list = []  # 获取区域信息
    for item in area_quest:
        # 检查日期是否是当前日期
        start_date = timezone.datetime.today()  # 当前日期
        ent_date = start_date + timezone.timedelta(days=1)  # 当前日期加1天
        start_date = start_date.strftime('%Y-%m-%d')
        ent_date = ent_date.strftime('%Y-%m-%d')  # 日期格式化成 2020-01-07
        # 获取检查结果
        check_number = msafety.CheckRecord.objects.filter(area_id=item["id"], area__emp__wechat=wechat_user_id,
                                                          create_date__range=(start_date, ent_date)).count()

        area_list.append({"area": item, "check_number": check_number})

    return render(request, 'safety/inspect.html', {'name': emp["name"], "area_list": area_list})


@csrf_exempt
def inspect_form(request):
    if request.method == 'GET':
        wechat_user_id = request.session.get('wechat_user_id')
        emp = request.session.get('emp')

        scan_code_str = request.GET.get('scanCodeStr')  # 扫描结果
        area_id = request.GET.get('area_id')
        area_name = request.GET.get('area_name')
        if scan_code_str:  # 如果是扫描过来的，从数据库中获取 区域信息
            area = msafety.Area.objects.filter(barcode=scan_code_str).first()
            area_id = area.id
            area_name = area.name

        if wechat_user_id:
            if area_id and area_name:
                return render(request, 'safety/inspect_form.html',
                              {"area_id": area_id, "area_name": area_name, "userId": wechat_user_id,
                               "name": emp["name"]})
            else:
                return redirect('/webapp/inspect/')
        else:
            return redirect('/webapp/inspect/')

    if request.method == 'POST':  # 上报数据
        data = request.POST.get('data')  # 获取数据
        if data:
            data = json.loads(data)  # 将数据转成json格式
            emp = request.session.get('emp')
            state = True  # 默认状态是好的
            if data["isWarning"] == 'on':  # 如果状态不好
                state = False
            # 保存记录
            try:
                result_check_record = msafety.CheckRecord.objects.create(
                    **{'emp_id': emp['pk'], 'area_id': data["area_id"], "state": state,
                       "description": data["warningContent"]})
            except Exception:
                return HttpResponse(0)
            if result_check_record:
                img_name_list = data["imgNames"]
                for img_name in img_name_list:
                    msafety.CheckImage.objects.create(
                        **{"check_record_id": result_check_record.pk, "img": img_name})
            return HttpResponse(result_check_record.pk)  # 成功返回记录的ID
        return HttpResponse(0)


def check_record(request):
    """
    检查记录
    :param request:
    :return:
    """
    # 获取查询条件
    # 区域
    area = msafety.Area.objects.all().values('pk', 'name')  # 获取区域名称，用于前端选择
    check_list = ''
    print(area)
    if request.method == 'GET':
        current_date = timezone.datetime.today()  # 当前日期
        start_date = current_date - timezone.timedelta(days=1)  # 昨天
        check_list = msafety.CheckRecord.objects.filter(
            create_date__range=(start_date, current_date + timezone.timedelta(days=1))).values("pk", "create_date",
                                                                                               "state",
                                                                                               "area__name",
                                                                                               "emp__name",
                                                                                               "description", )

        for item in check_list:  # 获取对应的图片
            img_list = msafety.CheckImage.objects.values("img").filter(check_record=item["pk"])
            img = []
            for i in img_list:
                # print(i["img"])
                img.append(i["img"])
            item["img"] = img

    if request.method == 'POST':
        area_id = request.POST.get('area')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if not start_date and not end_date:
            check_list = msafety.CheckRecord.objects.filter(
                area_id=area_id).values("pk", "create_date",
                                        "state",
                                        "area__name",
                                        "emp__name",
                                        "description", )
        else:
            check_list = msafety.CheckRecord.objects.filter(
                create_date__range=(start_date, end_date)).values("pk", "create_date",
                                                                  "state",
                                                                  "area__name",
                                                                  "emp__name",
                                                                  "description", )
        for item in check_list:
            img_list = msafety.CheckImage.objects.values("img").filter(check_record=item["pk"])
            img = []
            for i in img_list:
                print(i["img"])
                img.append(i["img"])
            item["img"] = img
    return render(request, "safety/check_record.html", {"check_list": check_list, "area": area})
