#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/1/21 9:12
# @Author  : mark.hu
# @Site    : 
# @File    : 1、面向对象的封装.py
# @Software: PyCharm
# @Email:5898387@qq.com


class Base(object):
    """
        面向对象封装  方法  基础方法
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


class Foo(Base):
    """
        此对象继承 Base 对象，就拥有了Base对象的方法
    """

    def show_detail(self):
        """
        调用基础对象里面的方法，可以对方法进行修改
        :return:
        """
        msg = "我叫%s,来自月球." % self.name
        print(msg)


class Bar(Base):
    """
    单独的继承Base方法
    """
    pass


obj1 = Foo('mark')
obj1.show_detail()  # result: 我叫mark,来自月球.  注:此时方法被改变了

obj2 = Bar('王伟')
obj2.show_detail()  # result: 我叫王伟,来自地球.  注:依然使用的是Base基类的方法
