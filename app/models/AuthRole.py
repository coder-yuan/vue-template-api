#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  AuthRole.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  角色Model类
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.config.setting import DEFAULT_START_PAGE, DEFAULT_PAGE_SIZE
from app.helper.CommonHelper import get_accurated_dict
from app.models.AuthRolePermissions import AuthRolePermissions
from app.models.AuthUserRoles import AuthUserRoles
from app.extensions.BaseModel import BaseModel, session_commit
from app.models.AuthPermission import AuthPermission
from app.config.log.LoguruConfig import logger


class AuthRole(BaseModel):
    __tablename__ = 'auth_role'
    __table_args__ = {

        'mysql_engine': 'InnoDB'
    }

    code = Column('code', String(40), doc='角色编码')
    name = Column('name', String(50), doc='角色名称')
    permissions = relationship(
        'AuthPermission',
        secondary='auth_role_permissions',
        primaryjoin='and_(AuthRole.id==AuthRolePermissions.role_id, '
                    'AuthRolePermissions.status==0, '
                    'AuthPermission.status==0)',
        lazy='dynamic'
    )

    @staticmethod
    def get_default():
        default = AuthRole.query.filter(AuthRole.code == 'default')
        return default

    @staticmethod
    def get_by_code(_code):
        return AuthRole.query.filter_by(code=_code).first()

    @staticmethod
    def get_ids_by_code(role_codes):
        roles = AuthRole.query.filter(AuthRole.code.in_(role_codes)).all()
        return [role.id for role in roles]

    def add_permission(self, permission):
        self.permissions.append(permission)

    def add_permissions(self, permissions):
        for permission in permissions:
            self.add_permission(permission)

    def get_permissions(self):
        for permission in self.permission:
            yield permission

    def refresh_permissions(self, permission_ids):
        for permission in self.permissions:
            self.permissions.remove(permission)
        session_commit()

        for permission_id in permission_ids:
            permission = AuthPermission.get_by_status(permission_id)
            if not permission:
                permission = AuthPermission(id=permission_id)
            self.permissions.append(permission)

        return session_commit()

    @staticmethod
    def get_permission_by_user_id(user_id):
        permissions = AuthPermission.query \
            .join(AuthRolePermissions, AuthRolePermissions.permission_id == AuthPermission.id) \
            .join(AuthRole, AuthRole.id == AuthRolePermissions.role_id) \
            .join(AuthUserRoles, AuthRole.id == AuthUserRoles.role_id) \
            .filter(AuthUserRoles.user_id == user_id).all()
        return permissions

    @classmethod
    def get_pagination(cls, start=DEFAULT_START_PAGE, page_size=DEFAULT_PAGE_SIZE, **kwargs):
        result = None

        accurated_dict, kwargs = get_accurated_dict([], **kwargs)

        try:
            # 精确查询部分处理
            q = cls.query.filter_by(**accurated_dict)

            # 模糊匹配部分处理
            if 'code' in kwargs:
                q = q.filter(cls.code.like('%' + kwargs['code'] + '%'))

            if 'name' in kwargs:
                q = q.filter(cls.name.like('%' + kwargs['name'] + '%'))

            return q.order_by(cls.created_time.desc()).paginate(start, page_size, error_out=False)

        except Exception as e:
            logger.error(e)
        return result

    #
    # @staticmethod
    # def get_permissions_by_roles_id(role_ids):
    #     permissions = AuthPermission.query.filter_by().distinct().join(
    #         AuthRolePermissions, AuthRolePermissions.permission_id == AuthPermission.id).filter(
    #         and_(
    #             AuthRolePermissions.role_id.in_(role_ids),
    #             AuthRole.status == 0,
    #             AuthPermission.status == 0)).all()
    #     return permissions
    #
    # @staticmethod
    # def get_permissions_by_roles_name(role_names):
    #     role_ids = AuthRole.get_ids_by_code(role_names)
    #
    #     permissions = AuthPermission.query.filter_by().distinct().join(
    #         AuthRolePermissions,
    #         AuthRolePermissions.permission_id == AuthPermission.id).filter(
    #         and_(AuthRolePermissions.role_id.in_(role_ids),
    #              AuthRole.status == 0,
    #              AuthPermission.status == 0)).all()
    #     return permissions
