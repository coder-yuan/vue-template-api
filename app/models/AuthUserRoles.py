#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  UserRoles.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from app.extensions.BaseModel import BaseModel, session_commit


class AuthUserRoles(BaseModel):
    __tablename__ = 'auth_user_roles'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    user_id = Column('user_id', INTEGER(unsigned=True), ForeignKey('user.id'), doc='用户Id')
    role_id = Column('role_id', INTEGER(unsigned=True), ForeignKey('auth_role.id'), doc='角色Id')

    # def __init__(self, user_id=None, role_id=None):
    #     self.user_id = user_id
    #     self.role_id = role_id

    @staticmethod
    def delete_by_user_id(user_id):
        auth_roles = AuthUserRoles.query.filter_by(user_id=user_id).all()
        for auth_role in auth_roles:
            auth_role.delete()
        return session_commit()

    @staticmethod
    def delete_by_role_id(role_id):
        auth_roles = AuthUserRoles.query.filter_by(user_id=role_id).all()
        auth_roles.delete()
        return session_commit()

    @staticmethod
    def binding(user_id, role_ids):
        for role_id in role_ids:
            auth_role = AuthUserRoles(user_id=user_id, role_id=role_id, status=0)
            auth_role.save()

        return session_commit()
