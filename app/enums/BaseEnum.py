#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/15
# @File     :  ClientTypeEnum.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def get_name_by_value(cls, value):
        try:
            name = BaseEnum(value).name
        except ValueError as e:
            name = ''
        return name

    @classmethod
    def get_value_by_name(cls, name):
        try:
            value = BaseEnum[name].value
        except KeyError as e:
            value = None
        return value

    @classmethod
    def values(cls):
        return [e.value for e in cls]

    @classmethod
    def names(cls):
        return [e.name for e in cls]

    @classmethod
    def check_value_or_default(cls, value):
        return value if value in cls.values() else cls.DEFAULT.value

