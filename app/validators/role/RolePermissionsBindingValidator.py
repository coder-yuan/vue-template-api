#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/12
# @File     :  UserRegisterValidator.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  角色权限绑定参数验证
from app.extensions.BaseValidator import BaseValidator


class RolePermissionsBindingValidator(BaseValidator):
    """
    角色权限绑定参数验证
    """

    # 角色权限绑定参数验证Schema
    ValidatorSchema = {
        "type": "object",
        "required": ["data"],
        "properties": {
            "data": {
                "type": "object",
                "required": ["role_id", "permissions"],
                "properties": {
                    "role_id": {
                        "type": "integer"
                    },
                    "permissions": {
                        "anyOf": [
                            {"type": "array",
                             "items": {
                                 "type": "integer"
                             }},
                            {"type": "null"}]
                    }
                }
            }
        }
    }

    @staticmethod
    def validator(data, schema=None, _classname=None):
        schema = schema if schema else RolePermissionsBindingValidator.ValidatorSchema
        _classname = _classname if _classname else __class__.__name__
        return super(RolePermissionsBindingValidator, RolePermissionsBindingValidator).validator(data, schema,
                                                                                                 _classname)
