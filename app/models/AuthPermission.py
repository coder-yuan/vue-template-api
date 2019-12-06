#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  AuthRole.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  权限Model类
from sqlalchemy import Column, String, ForeignKey, desc
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from app.config.setting import DEFAULT_START_PAGE, DEFAULT_PAGE_SIZE
from app.helper.CommonHelper import get_accurated_dict
from app.extensions.BaseModel import BaseModel
from app.config.log.LoguruConfig import logger


class AuthPermission(BaseModel):
    __tablename__ = 'auth_permission'
    __table_args__ = {

        'mysql_engine': 'InnoDB'
    }

    code = Column('code', String(40), doc='权限编码')
    name = Column('name', String(50), doc='权限名称')
    type = Column('type', TINYINT, doc='权限类型 0 -- menu, 1 -- 后台接口， 2 -- 其他')
    node_url = Column('node_url', String(255), doc='资源地址')
    method = Column('method', String(10), doc='访问方法')

    # 以下为菜单时使用
    parent_id = Column('parent_id', INTEGER(unsigned=True), ForeignKey('auth_permission.id'), doc='父节点Id')
    menu_level = Column('menu_level', INTEGER(unsigned=True), doc='菜单层级')
    menu_order = Column('menu_order', INTEGER(unsigned=True), doc='菜单顺序')

    children = relationship('AuthPermission')

    @classmethod
    def get_pagination(cls, start=DEFAULT_START_PAGE, page_size=DEFAULT_PAGE_SIZE, **kwargs):
        result = None

        accurated_dict, kwargs = get_accurated_dict(['method', 'type'], **kwargs)

        try:
            # 精确查询部分处理
            q = cls.query.filter_by(**accurated_dict)

            # 模糊匹配部分处理
            if 'name' in kwargs:
                q = q.filter(cls.name.like('%' + kwargs['name'] + '%'))

            if 'code' in kwargs:
                q = q.filter(cls.code.like('%' + kwargs['code'] + '%'))

            if 'node_url' in kwargs:
                q = q.filter(cls.node_url.like('%' + kwargs['node_url'] + '%'))

            return q.order_by(desc(cls.created_time)).paginate(start, page_size, error_out=False)

        except Exception as e:
            logger.error(e)
        return result

    @classmethod
    def get_by_code(cls, code):
        return AuthPermission.query.filter_by(code=code).first()

    @classmethod
    def get_by_parent_id(cls, id):
        return AuthPermission.query.filter_by(parent_id=id).all()
