#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'mark'
__mtime__ = '2020-02-09'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import hashlib


def get_md5(origin):
    """
    md5加密
    :param origin:
    :return:
    """
    #ha = hashlib.md5(b'mark_is_a_genius')  # b'mark_is_a_genius' 加盐
    ha = hashlib.md5()
    ha.update(origin.encode('utf-8'))  # encode('utf-8') 转换成字节
    return ha.hexdigest()
