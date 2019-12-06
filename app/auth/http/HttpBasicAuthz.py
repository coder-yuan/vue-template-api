#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  HttpBasicAuthz
# @Author   :  jackeroo
# @Time     :  2019/11/27 9:08 下午
# @File     :  HttpBasicAuthz.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :
from flask import Response
from flask_httpbasicauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from app.config.json.Json import jsonpickle
from app.enums.ResultEnum import ResultEnum
from app.helper.ModelHelper import model_to_dict
from app.helper.ResultHelper import ResultHelper
from app.models.User import User

auth = HTTPBasicAuth()
auth.hash_password(generate_password_hash)
auth.verify_password(check_password_hash)


# HttpBasicAuth的认证错误提示
# 必须返回一个http response
@auth.error_handler
def login_error():
    content = jsonpickle.encode(ResultHelper.error_with_enum(ResultEnum.TOKEN_VALIDATE_ERROR), unpicklable=False,
                                max_depth=20)
    resp = Response(
        content,
        mimetype='application/json'
    )

    return resp


@auth.get_user
def get_user(request, username):
    user = User.get_by_account(username)
    if not user:
        return None
    return model_to_dict(user, handle_relationship_flag=True)
