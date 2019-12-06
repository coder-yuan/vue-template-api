#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/12
# @File     :  UserRegisterValidator.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  客户端注册/登录参数验证
from app.enums.ClientTypeEnum import ClientTypeEnum
from app.extensions.BaseValidator import BaseValidator


class ClientRegisterValidator(BaseValidator):
    """
    客户端注册/登录参数验证
    """

    # 客户端注册/登录参数验证Schema
    ValidatorSchema = {
        "type": "object",
        "required": ["data"],
        "properties": {
            "data":
                {
                    "type": "object",
                    "required": ["account", "password", "client_type"],
                    "properties": {
                        "account": {
                            "type": "string"
                        },
                        "password": {
                            "type": "string"
                        },
                        "client_type": {
                            "type": "integer",
                            "enum": [
                                ClientTypeEnum.USER_NORMAL.value,
                                ClientTypeEnum.USER_EMAIL.value,
                                ClientTypeEnum.USER_MOBILE.value,
                                ClientTypeEnum.USER_MINA.value,
                                ClientTypeEnum.USER_WECHAT.value,
                                ClientTypeEnum.USER_MISC.value]
                        }
                    }
                }
        }
    }

    @staticmethod
    def validator(data, schema=None, _classname=None):
        schema = schema if schema else ClientRegisterValidator.ValidatorSchema
        _classname = _classname if _classname else __class__.__name__
        return super(ClientRegisterValidator, ClientRegisterValidator).validator(data, schema, _classname)


if __name__ == '__main__':
    data = {
        "data": {
            "account": "ccl",
            "password": "12345678",
            "level": 0,
            "client_type": 100
        }
    }

    ClientRegisterValidator.validator(data, ClientRegisterValidator.ValidatorSchema, __name__)
