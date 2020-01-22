#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/21 9:12
# @Author  : mark.hu
# @Site    : 
# @File    : 1、面向对象的封装.py
# @Software: PyCharm
# @Email:5898387@qq.com


class Foo(object):
    """
        面向对象封装  方法
    """

    def __init__(self, name):
        """
        # 初始化方法
        :param name:  需要传入的值
        """
        self.name = name

    def show_detail(self):
        """
        显示详细信息
        :return:
        """
        msg = "我叫%s,来自地球." % self.name
        print(msg)


# 调用
obj1 = Foo('mark')
obj1.show_detail()  # 我叫mark,来自地球.

obj2 = Foo('王伟')
obj2.show_detail()  # 我叫王伟,来自地球.
