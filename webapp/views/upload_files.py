#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 9:08
# @Author  : mark.hu
# @Site    : 
# @File    : upload_files.py
# @Software: PyCharm
# @Emial:5898387@qq.com

from django.shortcuts import render, HttpResponse, redirect
from django.conf import settings
import base64, os


def upload_img(request):
    ''' 上传图片
    :param request:
    :return: 成功返回文件名，失败返回0
    '''
    if request.method == 'POST':
        images = request.POST.get('images')
        file_name = request.POST.get('fileName')
        try:
            # 传来的图中有现拍的，也有其它图片，需要在这里判断一下
            if "data" in str(images):
                il = str(images).split(',')
                img = il[1]
            else:
                img = images
            # 路径
            path = settings.BASE_DIR + settings.MEDIA_URL + file_name
            # 存入图片
            with open(path, 'wb+') as f:
                f.write(base64.b64decode(img))
            return HttpResponse(file_name)
        except Exception:
            return HttpResponse(0)


def upload_img_del(request):
    """
     删除图片
    :param request:
    :return:
    """
    print(request)
    if request.method == 'POST':
        image_name = request.POST.get('image_name')
        if image_name:
            media_path = os.path.join(settings.BASE_DIR, 'media')
            path = os.path.join(media_path, image_name)
            if os.path.exists(path):
                os.remove(path)
                return HttpResponse(1)
        return HttpResponse(0)
