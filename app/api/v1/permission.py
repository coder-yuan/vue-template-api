#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  
# @Author   :  jackeroo
# @Time     :  2019/11/20 下午5:42
# @File     :  permission.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :
from flask import g
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.auth.role_permission.PermissionDecorator import permission_accept
from app.enums.ResultEnum import ResultEnum
from app.helper.HttpHelper import HttpHelper
from app.helper.ModelHelper import pagination_to_dict, model_to_dict
from app.libs.handler.APIException import APIException
from app.libs.redprint import RedPrint
from app.models.AuthPermission import AuthPermission
from app.extensions.BaseValidator import json_validator
from app.validators.permission.PermissionValidator import PermissionValidator
from app.config.log.LoguruConfig import logger

api = RedPrint('permission')


@api.route('/<int:permission_id>', methods=['GET'])
@jwt_required
@permission_accept('permission:list')
def get_permission_by_id(permission_id):
    permissions = {}

    if permission_id:
        permissions = AuthPermission.get_by_status_or_404(permission_id)

    permissions_dict = model_to_dict(permissions, handle_relationship_flag=True)
    return HttpHelper.normal_handler(permissions_dict)


@api.route('', methods=['GET'])
@jwt_required
def get_permission():
    permissions = {}
    jwt_data = get_jwt_identity()
    user_id = jwt_data.get('id')
    if user_id:
        from app.models.AuthRole import AuthRole
        permissions = AuthRole.get_permission_by_user_id(user_id)

    return HttpHelper.normal_handler(permissions)


@api.route('/all', methods=['POST'])
@jwt_required
@permission_accept('permission:list')
@json_validator(PermissionValidator.ValidatorSchema)
def get_all_permission():
    query_data = g.json_data
    start, pagesize = HttpHelper.get_page_info()

    if query_data:
        paginated_obj = AuthPermission.get_pagination(start, pagesize, **query_data)
    else:
        paginated_obj = AuthPermission.get_pagination(start, pagesize)
    return HttpHelper.normal_handler(pagination_to_dict(paginated_obj))


@api.route('', methods=['POST'])
@jwt_required
@permission_accept('permission:add')
@json_validator(PermissionValidator.ValidatorSchema)
def add_permission():
    permission_data = g.json_data

    # Permission code cannot be empty
    code = permission_data.get('code', None)
    if not code:
        raise APIException(ResultEnum.PERMISSION_EMPTY_CODE)

    # Always existing permission with same code
    permission = AuthPermission.get_by_code(code)
    if permission:
        raise APIException(ResultEnum.PERMISSION_CODE_EXISTS)

    permission = AuthPermission()
    try:

        if 'id' in permission_data:
            del permission_data['id']

        permission.save(**permission_data)
        return HttpHelper.normal_handler(permission)
    except Exception as e:
        logger.error(e)
        raise APIException(ResultEnum.UNKNOWN_ERROR, e.args)


@api.route('/<int:permission_id>', methods=['POST'])
@jwt_required
@permission_accept('permission:edit')
@json_validator(PermissionValidator.ValidatorSchema)
def edit_permission(permission_id):
    permission_data = g.json_data
    if permission_data.get('id') != permission_id:
        raise APIException(ResultEnum.PERMISSION_INVALID_ID)

    permission = AuthPermission.get_by_status_or_404(permission_id)

    if 'code' in permission_data:
        permission_by_code = AuthPermission.get_by_code(permission_data.get('code'))
        if permission.id != permission_by_code.id:
            raise APIException(ResultEnum.PERMISSION_CODE_EXISTS)

    try:
        permission.update(**permission_data)
        return HttpHelper.normal_handler(permission)
    except Exception as e:
        logger.error(e)
        raise APIException(ResultEnum.UNKNOWN_ERROR, e.args)


@api.route('/<int:permission_id>', methods=['DELETE'])
@jwt_required
@permission_accept('permission:delete')
@json_validator(PermissionValidator.ValidatorSchema)
def delete_permission(permission_id):
    permission_data = g.json_data
    if permission_data.get('id') != permission_id:
        raise APIException(ResultEnum.PERMISSION_INVALID_ID)

    permission = AuthPermission.get_by_status_or_404(permission_id)
    try:
        permission.delete()
        return HttpHelper.normal_handler(permission)
    except Exception as e:
        logger.error(e)
        raise APIException(ResultEnum.UNKNOWN_ERROR, e.args)


@api.route('/<int:permission_id>', methods=['PATCH'])
@jwt_required
@permission_accept('permission:disable')
@json_validator(PermissionValidator.ValidatorSchema)
def disable_permission(permission_id):
    permission_data = g.json_data
    if permission_data.get('id') != permission_id:
        raise APIException(ResultEnum.PERMISSION_INVALID_ID)

    permission = AuthPermission.get_or_404(permission_id)
    try:
        permission.toggle_disable()
        return HttpHelper.normal_handler(permission)
    except Exception as e:
        logger.error(e)
        raise APIException(ResultEnum.UNKNOWN_ERROR, e.args)
