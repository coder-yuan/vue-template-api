#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/15
# @File     :  __init__.py.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
from flask import Blueprint

from app.api.v1 import token, user, client, role, permission, file, file_uploads, task


def reg_api_blueprint_v1():
    api_blueprint_v1 = Blueprint('api_blueprint_v1', __name__)

    token.api.register(api_blueprint_v1, url_prefix='/token')
    user.api.register(api_blueprint_v1, url_prefix="/user")
    client.api.register(api_blueprint_v1, url_prefix='/client')
    role.api.register(api_blueprint_v1, url_prefix='/role')
    permission.api.register(api_blueprint_v1, url_prefix='/permission')
    file.api.register(api_blueprint_v1, url_prefix='/files')
    file_uploads.api.register(api_blueprint_v1, url_prefix='/file')
    task.api.register(api_blueprint_v1, url_prefix='/task')

    return api_blueprint_v1
