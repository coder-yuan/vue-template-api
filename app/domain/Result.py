#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  Result.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  结果返回数据结构定义类
from typing import TypeVar

from app.enums.ResultEnum import ResultEnum

T = TypeVar('T')


class Result:

    def __init__(self, msg: str, code: int, error_code: int, data: T = None):
        self.success = True if code == 200 else False
        self.code = code
        self.msg = msg
        self.error_code = error_code
        self.data = data

    @classmethod
    def success(cls, data: T):
        return cls(ResultEnum.SUCCESS.value.msg, ResultEnum.SUCCESS.value.code, ResultEnum.SUCCESS.error_code, data)

    @classmethod
    def success_ex(cls, msg, data: T):
        return cls(msg, ResultEnum.SUCCESS.value.code, ResultEnum.SUCCESS.error_code, data)

    @classmethod
    def error_with_enum(cls, result_enum: ResultEnum, data: T = None):
        cls.code = result_enum.code
        cls.error_code = result_enum.error_code
        cls.msg = result_enum.msg
        cls.data = data
        return cls(cls.msg, cls.code, cls.error_code, cls.data)

    def isSuccess(self):
        return self.success
