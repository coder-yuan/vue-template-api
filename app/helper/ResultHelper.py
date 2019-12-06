#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  ResultHelper.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  结果返回处理类
from typing import TypeVar

from app.domain.Result import Result
from app.enums import ResultEnum

T = TypeVar('T')


class ResultHelper:

    @staticmethod
    def success(data: T):
        # 成功的时候调用
        return Result.success(data)

    @staticmethod
    def success_ext(data: T, msg):
        return Result.success_ex(msg, data)

    @staticmethod
    def error_with_enum(result_enum: ResultEnum, data: T = None):
        # 错误的时候调用
        return Result.error_with_enum(result_enum, data)

    @staticmethod
    def error_with_code(code: int, msg: str, data: T = None):
        # 未知错误，返回code和errmsg
        return Result(msg, code,  data)
