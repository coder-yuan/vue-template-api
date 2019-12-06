#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  Jackeroo
# @Time     :  2019/11/15
# @File     :  APIException.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  APIException异常处理模块
from app.config.json.Json import jsonpickle
from flask import request
from werkzeug.exceptions import HTTPException

from app.enums.ResultEnum import ResultEnum


class APIException(HTTPException):
    default_code = 200
    default_error_code = 500
    default_msg = 'sorry, we make a mistake (*￣︶￣)!'

    def __init__(self, result_enum=None, code=None, error_code=None, msg=None, data=None, headers=None):
        if result_enum:
            self.result_enum = result_enum
            self.code = result_enum.code
            self.error_code = result_enum.error_code
            self.msg = result_enum.msg
        else:
            self.code = code if code else APIException.default_code
            self.error_code = error_code if error_code else APIException.default_error_code
            self.msg = msg if msg else APIException.default_msg

        self.msg = msg if msg else self.msg
        self.data = data
        self.headers = headers
        super(APIException, self).__init__(self.data)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param(),
            data=self.data
        )

        return jsonpickle.encode(body)

    def get_headers(self, environ=None):
        headers = [
            ('Content-Type', 'application/json')
        ]
        return headers

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]


class Success(APIException):
    def __init__(self):
        self.result_enum = ResultEnum.SUCCESS

    def __call__(self, *ags, **kwargs):
        super(Success, self).__init__(result_enum=self.result_enum)


class NotFound(APIException):

    def __init__(self):
        self.result_enum = ResultEnum.USER_NOT_FOUND_ERROR

    def __call__(self, *args, **kwargs):
        super(NotFound, self).__init__(result_enum=self.result_enum)


class AuthFailed(APIException):

    def __init__(self):
        self.result_enum = ResultEnum.TOKEN_VALIDATE_ERROR

    def __call__(self, *args, **kwargs):
        super(AuthFailed, self).__init__(result_enum=self.result_enum)


class Forbidden(APIException):

    def __init__(self):
        self.result_enum = ResultEnum.FORBIDDEN

    def __call__(self, *args, **kwargs):
        super(Forbidden, self).__init__(result_enum=self.result_enum)
