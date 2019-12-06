#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  RolePermissions.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from app.extensions.BaseModel import BaseModel


class AuthRolePermissions(BaseModel):
    __tablename__ = 'auth_role_permissions'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    role_id = Column('role_id', INTEGER(unsigned=True), ForeignKey('auth_role.id'), doc='角色Id')
    permission_id = Column('permission_id', INTEGER(unsigned=True), ForeignKey('auth_permission.id'), doc='权限Id')

    @classmethod
    def get_by_role_id(cls, role_id):
        return AuthRolePermissions.query.filter_by(role_id=role_id).all()
