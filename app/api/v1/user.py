#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/15
# @File     :  user.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
from flask import g
from flask_jwt_extended import jwt_required
from werkzeug.security import generate_password_hash

from app.auth.role_permission.PermissionDecorator import permission_accept, roles_accept
from app.config.log.LoguruConfig import logger
from app.config.json.Json import jsonpickle
from app.config.setting import BASE_URL
from app.enums.ClientTypeEnum import ClientTypeEnum
from app.enums.ResultEnum import ResultEnum
from app.enums.UserLevelEnum import UserLevelEnum
from app.helper.HttpHelper import HttpHelper
from app.helper.ModelHelper import pagination_to_dict
from app.helper.ResultHelper import ResultHelper
from app.libs.handler.APIException import APIException
from app.libs.redprint import RedPrint
from app.models.AuthRole import AuthRole
from app.models.AuthUserRoles import AuthUserRoles
from app.models.User import User
from app.task.workers import send_welcome_email
from app.extensions.BaseValidator import json_validator
from app.validators.client.ClientRegisterValidator import ClientRegisterValidator
from app.validators.user.UserQueryValidator import UserQueryValidator
from app.validators.user.UserRolesBindingValidator import UserRolesBindingValidator
from app.validators.user.UserRegisterValidator import UserRegisterValidator

api = RedPrint('user')


def del_keys(json, keys):
    r = dict(json)
    for key in keys:
        if key in r:
            del r[key]
    return r


@api.route('/register', methods=['POST'])
@jwt_required
@permission_accept('user:add')
@json_validator(ClientRegisterValidator.ValidatorSchema)
def register():
    """
    用户注册
    :return: json
    """

    reg_info = g.json_data
    username = reg_info['account']
    password = reg_info['password']

    password = generate_password_hash(password)

    # 获取用户level
    level = reg_info.get('level')
    level = UserLevelEnum.check_value_or_default(level)

    # 获取用户类型
    client_type = reg_info.get('client_type')
    client_type = ClientTypeEnum.check_value_or_default(client_type)

    u1 = User.get_by_account(username)

    if u1:
        usr = {'id': u1.id, 'name': u1.account}
        return HttpHelper.error_handler(ResultEnum.USER_ALREADY_EXIST_ERROR, data=usr)

    # 已经算出了加密密码，用户属性字典中去掉password属性，否则保存将覆盖
    usr = User(account=username, password=password, level=level, client_type=client_type)
    user_dict = del_keys(reg_info, ['password', 'client_type'])
    result = usr.save(**user_dict)

    if not usr.id:
        return HttpHelper.error_handler(ResultEnum.USER_REGISTER_ERROR, data=result)

    # 添加默认的角色
    default_role = AuthRole.get_default().first()
    auth_user_role = AuthUserRoles(role_id=default_role.id, user_id=usr.id, status=0)
    auth_user_role.save()

    ret_user = {'id': usr.id, 'name': usr.account, 'role': default_role}
    return HttpHelper.json_response(ResultHelper.success(ret_user))


@api.route('/<int:user_id>', methods=['GET'])
@jwt_required
@roles_accept('default')
def get_user(user_id):
    """
    获取用户信息
    :return: json
    """

    u = User.get_by_status(user_id)
    logger.debug(jsonpickle.encode(u, unpicklable=False))
    user_dict = u.as_dict(handle_relationship_flag=True)
    avatar_img = user_dict.get('avatar_img').get('file_url')
    user_dict['avatar_img'] = BASE_URL + avatar_img
    return HttpHelper.normal_handler(user_dict)


@api.route('/<int:user_id>/roles', methods=['GET'])
@jwt_required
@permission_accept('role:list')
def get_user_roles(user_id):
    """
    获取用户信息
    :return: json
    """

    u = User.get_by_status_or_404(user_id)
    usr_dict = u.as_dict()
    usr_dict['roles'] = [role.as_dict() for role in u.roles]

    logger.debug(jsonpickle.encode(usr_dict, unpicklable=False))
    return HttpHelper.normal_handler(usr_dict)


@api.route('/<int:user_id>', methods=['POST'])
@jwt_required
@permission_accept('user:edit')
@json_validator(UserRegisterValidator.ValidatorSchema)
def edit_user(user_id):
    reg_info = g.json_data

    u1 = User.get_by_status_or_404(user_id)

    # 密码不通过这种方式修改，删除提交的密码信息
    user_dict = del_keys(reg_info, ['password', 'roles', 'avatar_img'])
    u1.update(**user_dict)

    return HttpHelper.json_response(ResultHelper.success(u1))


@api.route('/<int:user_id>', methods=['DELETE'])
@jwt_required
@permission_accept('user:delete')
def delete_user(user_id):
    usr = User.get_by_status_or_404(user_id)
    usr.delete()
    return HttpHelper.normal_handler()


@api.route('', methods=['POST'])
@jwt_required
@permission_accept('user:list')
@json_validator(UserQueryValidator.ValidatorSchema)
def get_users():
    """
    获取用户列表，分页返回
    :return: json
    """
    query_data = g.json_data

    start, pagesize = HttpHelper.get_page_info()

    if query_data:
        paginated_user = User.get_pagination_user(start, pagesize, **query_data)
    else:
        paginated_user = User.get_pagination_user(start, pagesize)
    return HttpHelper.normal_handler(pagination_to_dict(paginated_user))


@api.route('/<int:user_id>', methods=['PATCH'])
@jwt_required
@permission_accept('user:disable')
def disable_user(user_id):
    usr = User.get_by_status_or_404(user_id)

    usr.toggle_disable()
    return HttpHelper.normal_handler()


@api.route('/<int:user_id>/change', methods=['POST'])
@jwt_required
@permission_accept("user:edit")
@json_validator(UserRegisterValidator.ValidatorSchema)
def change_password(user_id):
    usr = User.get_by_status_or_404(user_id)

    password = g.json_data.get('password', None)
    if not password:
        raise APIException(ResultEnum.USER_OR_PASS_EMPTY_ERROR)

    usr.password = generate_password_hash(password)

    try:
        usr.update()
        return HttpHelper.normal_handler(usr)
    except Exception as e:
        logger.error(e)
        return HttpHelper.error_handler(ResultEnum.UNKNOWN_ERROR)


@api.route('/<int:user_id>/roles', methods=['POST'])
@jwt_required
@permission_accept("user:bind:role")
@json_validator(UserRolesBindingValidator.ValidatorSchema)
def bind_user_roles(user_id):
    json_data = g.json_data
    if user_id != json_data.get('user_id'):
        raise APIException(ResultEnum.USER_INVALID_ID)

    role_ids = json_data.get('roles')

    if not role_ids:
        raise APIException(ResultEnum.INVALID_PARAMETER)

    try:
        user = User.get_by_status_or_404(user_id)
        user.refresh_roles(role_ids)
        return HttpHelper.normal_handler()
    except Exception as e:
        logger.error(e)
        return HttpHelper.error_handler(ResultEnum.UNKNOWN_ERROR)


@api.route('/<int:user_id>/email', methods=['GET'])
@jwt_required
def send_mail(user_id):
    task = send_welcome_email.delay('Hello', user_id, 'http://localhost:9000/')

    return HttpHelper.normal_handler({'task_id': task.id})
