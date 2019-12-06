#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/11
# @File     :  JwtHelper.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  Jwt使用工具类
import time
import jwt

from app.enums.ResultEnum import ResultEnum
from app.helper import ResultHelper
from app.models.User import User


def verify_wxapp(username, password):
    return None


def create_token(request):
    grant_type = request.json.get('grant_type')
    username = request.json.get('username')
    password = request.json.get('password')

    if grant_type == 'password':
        result = User.verify_password(username, password)
    elif grant_type == 'wxapp':
        result = verify_wxapp(username, password)
    else:
        return ResultHelper.ResultHelper.error_with_code(404, '无效的grant_type', None)

    if not result.isSuccess():
        return result

    user = result.data
    payload = {
        'iss': 'sunforworld.com',
        'iat': int(time.time()),
        'exp': int(time.time() + 86400 * 7),
        'aud': 'www.sunforworld.com',
        'sub': user['id'],
        'username': user['username'],
        'scopes': ['open']
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return ResultHelper.ResultHelper.success(token)


def verify_bearer_token(token):
    payload = jwt.decode(token, 'secret', audience='www.sunforworld.com', algorithms=['HS256'])

    if payload:
        return ResultHelper.ResultHelper.success(payload)
    else:
        return ResultHelper.ResultHelper.error_with_enum(ResultEnum.TOKEN_VALIDATE_ERROR)
