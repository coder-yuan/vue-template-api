#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/12
# @File     :  BaseValidator.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
import inspect
from functools import wraps

from flask import request, g
from jsonschema import validate, SchemaError, ValidationError
from app.config.log.LoguruConfig import logger
from app.enums.ResultEnum import ResultEnum
from app.libs.handler.APIException import APIException
from app.config.json.Json import jsonpickle


class BaseValidator:

    @staticmethod
    def validator(data, _schema, _classname):
        try:
            validate(data, _schema)
        except ValueError as e:
            logger.warning("%s ValueError: %s" % (_classname, e.args))
            raise APIException(ResultEnum.INVALID_PARAMETER, data=e.args)
        except (SchemaError, ValidationError) as se:
            logger.warning("%s SchemaError: %s" % (_classname, se.message))
            raise APIException(ResultEnum.INVALID_PARAMETER, data=se.message)

        return data['data']


def json_validator(validator_schema):
    """
    | 本注解需要保证当前用户已经登录，并且具备相应的权限 |.

    示例::

        @route('/user')
        @permission_accept('Admin', 'Agent')
        def escape_capture():  # User 需要具备Admin或者Agent权限
            ...

    | Calls get_jwt_identity获取token认证信息
    | Calls 如果出现异常或者没有得到任何信息，会抛出TOKEN_VALIDATE_ERROR
    | Calls 调用正常的业务流程.
    """

    def decorator(f):
        @wraps(f)  # Tells debuggers that is is a function wrapper
        def wrapper(*args, **kwargs):

            if not request.data:
                raise APIException(ResultEnum.JSON_SCHEMA_VALIDATION_ERROR)

            current_json_data = jsonpickle.decode(request.data)

            if not validator_schema or not current_json_data:
                raise APIException(ResultEnum.JSON_SCHEMA_VALIDATION_ERROR)

            # 把验证通过的json数据，挂载到flask的全局变量g上，以便其他后续访问
            g.json_data = BaseValidator.validator(current_json_data, validator_schema, None)

            # 超级管理员或者通过权限认证的用户，可以访问
            return f(*args, **kwargs)

        return wrapper

    return decorator
