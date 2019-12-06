#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/12
# @File     :  UserRegisterValidator.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  用户注册/登录参数验证
from app.extensions.BaseValidator import BaseValidator


class UserRegisterValidator(BaseValidator):
    """
    用户注册参数验证
    """

    # 用户注册/登录参数验证Schema
    ValidatorSchema = {
        "type": "object",
        "required": ["data"],
        "properties": {
            "data":
                {
                    "type": "object",
                    "properties": {
                        "account": {
                            "type": "string"
                        },
                        "address": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "avatar": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ]
                        },
                        "birthday": {
                            "anyOf": [
                                {"type": "string", "format": "date-time"},
                                {"type": "null"}
                            ]
                        },
                        "client_type": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ]
                        },
                        "created_time": {
                            "anyOf": [
                                {"type": "string", "format": "date-time"},
                                {"type": "null"}
                            ]
                        },
                        "deleted_time": {
                            "anyOf": [
                                {"type": "string", "format": "date-time"},
                                {"type": "null"}
                            ]
                        },
                        "dept_id": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ]
                        },
                        "disabled": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"},
                                {"type": "boolean"}
                            ]
                        },
                        "email": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "first_name": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "id": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ]
                        },
                        "last_login_time": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "last_name": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "level": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ]
                        },
                        "login_ip": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "mobile": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "nick_name": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "password": {
                            "type": "string"
                        },
                        "remark": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "sex": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ]
                        },
                        "status": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"},
                                {"type": "boolean"}
                            ]
                        },
                        "updated_time": {
                            "anyOf": [
                                {"type": "string", "format": "date-time"},
                                {"type": "null"}
                            ]
                        }
                    },
                    "required": ['account', 'password']
                }
        }
    }

    @staticmethod
    def validator(data, schema=None, _classname=None):
        schema = schema if schema else UserRegisterValidator.ValidatorSchema
        _classname = _classname if _classname else __class__.__name__
        return super(UserRegisterValidator, UserRegisterValidator).validator(data, schema, _classname)
