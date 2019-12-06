#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  
# @Author   :  jackeroo
# @Time     :  2019/11/20 下午2:55
# @File     :  PermissionDecorator.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :
import re
from functools import wraps

from flask import request

from app.config.log.LoguruConfig import logger
from flask_jwt_extended import get_jwt_identity
from app.enums.ResultEnum import ResultEnum
from app.libs.handler.APIException import APIException
from app.models.User import User


def check_allowed(certifications, allowed_certifications):
    checked = False

    for certification in certifications:
        if certification in allowed_certifications:
            checked = True
            break

    return checked


def get_current_jwt_user():
    """
    校验当前用户是否进行Jwt登录
    :return: 当前jwt登录用户信息
    """
    current_user = None
    try:
        current_user = get_jwt_identity()
    except Exception as e:
        logger.error(e)
    finally:
        if not current_user:
            raise APIException(ResultEnum.TOKEN_VALIDATE_ERROR)
    return current_user


def check_certification_in_or_die(certifications, accept_certifications):
    # 无权限直接抛拒绝访问异常
    if not certifications:
        raise APIException(ResultEnum.ACCESS_FORBIDDEN)

    # 通不过验证也抛出拒绝访问异常
    if not check_allowed(certifications, accept_certifications):
        raise APIException(ResultEnum.ACCESS_FORBIDDEN)


def roles_accept(*accept_role_names):
    """
    | 本注解需要保证当前用户已经登录，并且具备相应的权限 |.

    示例::

        @route('/user')
        @roles_required('Admin', 'Agent')
        def escape_capture():  # User 需要具备Admin或者Agent权限
            ...

    | Calls get_jwt_identity获取token认证信息
    | Calls 如果出现异常或者没有得到任何信息，会抛出TOKEN_VALIDATE_ERROR
    | Calls 调用正常的业务流程.
    """

    def wrapper(f):
        @wraps(f)  # Tells debuggers that is is a function wrapper
        def decorator(*args, **kwargs):
            current_user = get_current_jwt_user()

            # 不是超级管理员
            if not User.is_admin(current_user.get('level')):
                # 获取用户角色信息，权限验证不通过则抛出异常退出
                certifications = [role for role in current_user.get('roles')]
                check_certification_in_or_die(certifications, accept_role_names)

            # 超级管理员或者通过权限认证者可以访问
            return f(*args, **kwargs)

        return decorator

    return wrapper


def is_current_user(_id):
    url = request.base_url
    pattern = r'\/api\/v1\/user\/(\d+)'
    result = re.findall(pattern, url)
    if result and _id in result:
        return True

    return False


def permission_accept(*accept_permission_names):
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

    def wrapper(f):
        @wraps(f)  # Tells debuggers that is is a function wrapper
        def decorator(*args, **kwargs):
            current_user = get_current_jwt_user()

            # 不是超级管理员
            if not User.is_admin(current_user.get('level')) and not is_current_user(current_user.get('id')):
                # 必须有相应权限，否则抛出异常退出
                certifications = [role for role in current_user.get('permissions')]
                check_certification_in_or_die(certifications, accept_permission_names)

            # 超级管理员或者通过权限认证的用户，可以访问
            return f(*args, **kwargs)

        return decorator

    return wrapper
