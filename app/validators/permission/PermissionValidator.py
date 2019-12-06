#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/12
# @File     :  UserRegisterValidator.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :   权限修改、添加提交数据验证
from app.extensions.BaseValidator import BaseValidator


class PermissionValidator(BaseValidator):
    """
    权限修改、添加提交数据验证
    """

    # 权限修改、添加提交数据验证Schema
    ValidatorSchema = {
        "type": "object",
        "required": ["data"],
        "properties":
            {
                "data": {
                    "type": "object",
                    "required": ["name", "code"],
                    "properties": {
                        "name": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "code": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}]
                        },
                        "disabled": {
                            "anyOf": [
                                {"type": "boolean"},
                                {"type": "null"}
                            ]
                        },
                        "type": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ]
                        },
                        "node_url": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "method": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "menu_level": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ]
                        },
                        "menu_order": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ]
                        },
                        "parent_id": {
                            "anyOf": [
                                {"type": "integer"},
                                {"type": "null"}
                            ]
                        },
                        "remark": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "null"}
                            ]
                        },
                        "status": {
                            "anyOf": [
                                {"type": "boolean"},
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
                        "updated_time": {
                            "anyOf": [
                                {"type": "string", "format": "date-time"},
                                {"type": "null"}
                            ]
                        }
                    }
                }
            }
    }

    @staticmethod
    def validator(data, schema=None, _classname=None):
        schema = schema if schema else PermissionValidator.ValidatorSchema
        _classname = _classname if _classname else __class__.__name__
        return super(PermissionValidator, PermissionValidator).validator(data, schema, _classname)
