#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  : icode_flask_be
# @Software : PyCharm
# @File     : role.py
# @Author   : jackeroo
# @Time     : 2019/11/19 5:20 下午
# @Contact  : 
# @Desc     :
from flask import g
from flask_jwt_extended import jwt_required

from app.auth.role_permission.PermissionDecorator import permission_accept
from app.enums.ResultEnum import ResultEnum
from app.helper.HttpHelper import HttpHelper
from app.helper.ModelHelper import model_to_dict, pagination_to_dict
from app.libs.handler.APIException import APIException
from app.libs.redprint import RedPrint
from app.models.AuthPermission import AuthPermission
from app.models.AuthRole import AuthRole
from app.models.AuthRolePermissions import AuthRolePermissions
from app.extensions.BaseValidator import json_validator
from app.validators.role.RolePermissionsBindingValidator import RolePermissionsBindingValidator
from app.validators.role.RoleValidator import RoleValidator
from app.config.log.LoguruConfig import logger

api = RedPrint('role')


@api.route('/<int:role_id>', methods=['GET'])
@jwt_required
@permission_accept('role:list')
def get_role(role_id):
    """
    获取Role详情信息
    :param role_id:
    :return:
    """
    role = AuthRole.get_by_status(role_id)
    if not role:
        return HttpHelper.error_handler(ResultEnum.NOT_FOUND_ERROR)

    return HttpHelper.normal_handler(model_to_dict(role, handle_relationship_flag=True))


@api.route('/all', methods=['POST'])
@jwt_required
@permission_accept('role:list')
@json_validator(RoleValidator.ValidatorSchema)
def get_all_roles():
    """
    获取Role全部列表，因为内容不多，不进行分页展示
    :return:
    """
    query_data = g.json_data
    start, pagesize = HttpHelper.get_page_info()

    if query_data:
        paginated_obj = AuthRole.get_pagination(start, pagesize, **query_data)
    else:
        paginated_obj = AuthRole.get_pagination(start, pagesize)
    return HttpHelper.normal_handler(pagination_to_dict(paginated_obj))


@api.route('', methods=['POST'])
@jwt_required
@permission_accept('role:add')
@json_validator(RoleValidator.ValidatorSchema)
def add_role():
    role_data = g.json_data

    if 'name' not in role_data or 'code' not in role_data:
        raise APIException(ResultEnum.INVALID_PARAMETER)

    role_code = role_data.get('code')
    role_name = role_data.get('name')
    role = AuthRole.get_by_code(role_code)
    if role:
        raise APIException(ResultEnum.ROLE_CODE_EXIST)

    role = AuthRole(code=role_code, name=role_name)
    try:

        if 'id' in role_data:
            del role_data['id']

        role.save(**role_data)
        return HttpHelper.normal_handler(role)
    except Exception as e:
        logger.error(e)
        raise APIException(ResultEnum.UNKNOWN_ERROR, e.args)


@api.route('/<int:role_id>', methods=['POST'])
@jwt_required
@permission_accept('role:edit')
@json_validator(RoleValidator.ValidatorSchema)
def edit_role(role_id):
    role_data = g.json_data
    if role_data.get('id') != role_id:
        raise APIException(ResultEnum.ROLE_INVALID_ID)

    role = AuthRole.get_by_status_or_404(role_id)

    if 'code' in role_data:
        role_by_code = AuthRole.get_by_code(role_data.get('code'))
        if role.id != role_by_code.id:
            raise APIException(ResultEnum.ROLE_CODE_EXIST)
    try:
        role.update(**role_data)
        return HttpHelper.normal_handler(role)
    except Exception as e:
        logger.error(e)
        raise APIException(ResultEnum.UNKNOWN_ERROR, e.args)


@api.route('/<int:role_id>', methods=['DELETE'])
@jwt_required
@permission_accept('role:delete')
@json_validator(RoleValidator.ValidatorSchema)
def delete_role(role_id):
    role_data = g.json_data
    if role_data.get('id') != role_id:
        raise APIException(ResultEnum.ROLE_INVALID_ID)

    role = AuthRole.get_by_status(role_id)
    try:
        role.delete()
        return HttpHelper.normal_handler(role)
    except Exception as e:
        logger.error(e)
        raise APIException(ResultEnum.UNKNOWN_ERROR, e.args)


@api.route('/<int:role_id>', methods=['PATCH'])
@jwt_required
@permission_accept('role:disable')
@json_validator(RoleValidator.ValidatorSchema)
def disable_role(role_id):
    role_data = g.json_data
    if role_data.get('id') != role_id:
        raise APIException(ResultEnum.ROLE_INVALID_ID)

    role = AuthRole.get_by_status(role_id)
    try:
        role.toggle_disable()
        return HttpHelper.normal_handler(role)
    except Exception as e:
        logger.error(e)
        raise APIException(ResultEnum.UNKNOWN_ERROR, e.args)


@api.route('/<int:role_id>/permission', methods=['POST'])
@jwt_required
@json_validator(RolePermissionsBindingValidator.ValidatorSchema)
@permission_accept("role:bind:permission")
def bind_role_permissions(role_id):
    json_data = g.json_data
    if role_id != json_data.get('role_id'):
        raise APIException(ResultEnum.ROLE_INVALID_ID)

    permission_ids = json_data.get('permissions')

    if not permission_ids:
        raise APIException(ResultEnum.INVALID_PARAMETER)

    try:
        role = AuthRole.get_by_status_or_404(role_id)
        role.refresh_permissions(permission_ids)
        return HttpHelper.normal_handler()
    except Exception as e:
        logger.error(e)
        return HttpHelper.error_handler(ResultEnum.UNKNOWN_ERROR, e.args)


def get_permission_checked_dict(permissions_dict, checked_permission_ids):
    for index, permission in enumerate(permissions_dict):
        if permission.get('id') in checked_permission_ids:
            permission['checked'] = True
        else:
            permission['checked'] = False

        if 'children' in permission and permission['children']:
            permission['children'] = get_permission_checked_dict(permission['children'], checked_permission_ids)

        permissions_dict[index] = permission

    return permissions_dict


@api.route('/<int:role_id>/permission', methods=['GET'])
@jwt_required
@permission_accept('permission:list')
def get_all_permission_by_role_id(role_id):
    permissions = AuthPermission.get_by_parent_id(id=None)
    checked_permissions = AuthRolePermissions.get_by_role_id(role_id)
    checked_permission_ids = [checked_permission.permission_id for checked_permission in checked_permissions]

    permissions_dict = get_permission_checked_dict(
        [model_to_dict(permission, handle_relationship_flag=True) for permission in permissions],
        checked_permission_ids)

    return HttpHelper.normal_handler(permissions_dict)
