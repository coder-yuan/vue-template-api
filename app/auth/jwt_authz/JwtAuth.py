#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  
# @Author   :  jackeroo
# @Time     :  2019/11/20 下午1:28
# @File     :  JwtAuth.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :

from flask_jwt_extended import JWTManager

from app.enums.ResultEnum import ResultEnum
from app.helper.HttpHelper import HttpHelper

jwt = JWTManager()


# JWT 身份验证失败提示
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return HttpHelper.error_handler(ResultEnum.TOKEN_VALIDATE_ERROR)


@jwt.expired_token_loader
def expired_token(callback):
    return HttpHelper.error_handler(ResultEnum.TOKEN_EXPIRED_ERROR)


# Access Token需要更新提示
@jwt.needs_fresh_token_loader
def need_refresh_token(callback):
    return HttpHelper.error_handler(ResultEnum.TOKEN_NEED_REFRESH)
