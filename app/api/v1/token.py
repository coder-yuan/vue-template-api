#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/11
# @File     :  token.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  User相关Api
from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required,
                                get_jwt_identity)

from app.auth.http.HttpBasicAuthz import auth
from app.helper.HttpHelper import HttpHelper
from app.libs.redprint import RedPrint

api = RedPrint('token')


@api.route('', methods=['GET'])
@auth.login_required
def get_auth_token():
    """
    用户登录验证
    :return: json
    """
    usr = request.user
    roles = set()
    permissions = set()
    token_roles = usr.get('roles')

    for role in token_roles:
        roles.add(role.get('code'))
        for permission in role.get('permissions'):
            code = permission.get('code')
            permissions.add(code)

    data = {'id': usr.get('id'), 'username': usr.get('account'), 'roles': list(roles), 'permissions': list(permissions),
            'level': usr.get('level')}
    access_token = create_access_token(identity=data)
    refresh_token = create_refresh_token(identity=data)
    data['access_token'] = access_token
    data['refresh_token'] = refresh_token
    data['user'] = usr
    return HttpHelper.normal_handler(data)


@api.route('', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """
    Refresh the token
    :return:
    """
    current_user = get_jwt_identity()
    token = create_access_token(identity=current_user)

    return HttpHelper.normal_handler({"access_token": token})
