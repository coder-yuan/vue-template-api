#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/12
# @File     :  UserRegisterValidator.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  用户角色绑定参数验证
from app.extensions.BaseValidator import BaseValidator


class UserRolesBindingValidator(BaseValidator):
    """
    用户角色绑定参数验证
    """

    # 用户角色绑定参数验证Schema
    ValidatorSchema = {
        "type": "object",
        "required": ["data"],
        "properties": {
            "data": {
                "type": "object",
                "required": ["user_id", "roles"],
                "properties": {
                    "user_id": {
                        "type": "integer"
                    },
                    "roles": {
                        "type": "array",
                        "items": {
                            "type": "integer"
                        }
                    }
                }
            }
        }
    }

    @staticmethod
    def validator(data, schema=None, _classname=None):
        schema = schema if schema else UserRolesBindingValidator.ValidatorSchema
        _classname = _classname if _classname else __class__.__name__
        return super(UserRolesBindingValidator, UserRolesBindingValidator).validator(data, schema, _classname)
