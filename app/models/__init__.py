#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  __init__.py.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
from flask import Blueprint

# from app.models import Cabinet, Machine, OsType, User, AuthRole, AuthUserRoles, AuthPermission, AuthRolePermissions, \
#     AuthRolePermissions, AuthPermission

models = Blueprint('modules', __name__)
