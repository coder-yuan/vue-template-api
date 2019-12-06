#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  token.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  用户类
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.config.setting import ACCESS, DEFAULT_START_PAGE, DEFAULT_PAGE_SIZE
from app.enums.ResultEnum import ResultEnum
from app.helper.CommonHelper import get_accurated_dict
from app.libs.handler.APIException import APIException
from app.extensions.BaseModel import BaseModel, session_commit
from app.models.AuthRole import AuthRole
from app.config.log.LoguruConfig import logger


class User(BaseModel):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    first_name = Column('first_name', String(20), doc='用户名')
    last_name = Column('last_name', String(50), doc='姓')
    nick_name = Column('nick_name', String(50), doc='昵称')
    account = Column('account', String(20), doc='登录名')
    avatar = Column('avatar', INTEGER(unsigned=True), ForeignKey('sys_file.id'), doc='用户头像地址')
    email = Column('email', String(50), unique=True, doc='邮箱')
    login_ip = Column('login_ip', String(20), doc='登录IP地址')
    last_login_time = Column('last_login_time', DateTime, doc='最后登录时间')
    password = Column('password', String(255), doc='密码')
    mobile = Column('mobile', String(20), doc='联系电话')
    address = Column('address', String(255), doc='家庭住址')
    birthday = Column('birthday', DateTime, doc='生日')
    sex = Column('sex', TINYINT, doc='性别')
    client_type = Column('client_type', TINYINT, default=99, doc='客户端类型:  '
                                                                 '100 - normal (default)'
                                                                 '101 - email'
                                                                 '102 - mobile'
                                                                 '200 - wechat'
                                                                 '201 - mina'
                                                                 '300 - misc')
    level = Column('level', TINYINT, default=0, doc='用户级别:'
                                                    '0 -- 不允许访问'
                                                    '1 -- 普通用户 (默认) '
                                                    '99 -- 超级管理员')
    dept_id = Column('dept_id', INTEGER(unsigned=True), doc='组织/架构/公司/单位/部门 Id')

    roles = relationship(
        'AuthRole', secondary='auth_user_roles',
        primaryjoin='and_(User.id==AuthUserRoles.user_id, AuthUserRoles.status==0, AuthRole.status==0)',
        lazy='dynamic'
    )

    avatar_img = relationship(
        'SysFile',
        primaryjoin='and_(SysFile.id==User.avatar, SysFile.status==0)'
    )

    @staticmethod
    def get_by_account(account):
        return User.query.filter_by(account=account).first()

    def save(self, **kwargs):
        user = User.query.filter_by(account=self.account).first()
        if user:
            raise APIException(ResultEnum.USER_ALREADY_EXIST_ERROR, data=user)
        return super(User, self).save(**kwargs)

    def add_role(self, role):
        self.roles.append(role)

    def add_roles(self, roles):
        for role in roles:
            self.add_role(role)

    def get_roles(self):
        for role in self.roles:
            yield role

    def refresh_roles(self, role_ids):
        for role in self.roles:
            self.roles.remove(role)

        for role_id in role_ids:
            role = AuthRole.get_by_status(role_id)
            if not role:
                role = AuthRole(id=role_id)
            self.roles.append(role)

        return session_commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self.password

    def check_password(self, hashed_password, password):
        password = password if password else self.password
        return check_password_hash(hashed_password, password)

    @staticmethod
    def is_admin(level):
        return level == ACCESS['super_admin']

    def allowed(self, access_level):
        return self.level >= access_level

    @classmethod
    def get_pagination_user(cls, start=DEFAULT_START_PAGE, page_size=DEFAULT_PAGE_SIZE, **kwargs):
        result = None

        accurated_dict, kwargs = get_accurated_dict(['level', 'client_type'], **kwargs)

        try:

            # 精确查询部分处理

            q = cls.query.filter_by(**accurated_dict)

            # 模糊匹配部分处理
            if 'account' in kwargs:
                q = q.filter(User.account.like('%' + kwargs['account'] + '%'))

            if 'mobile' in kwargs:
                q = q.filter(User.mobile.like('%' + kwargs['mobile'] + '%'))

            if 'nick_name' in kwargs:
                q = q.filter(User.nick_name.like('%' + kwargs['nick_name'] + '%'))

            return q.order_by(cls.created_time.desc()).paginate(start, page_size, error_out=False)

        except Exception as e:
            logger.error(e)
        return result
