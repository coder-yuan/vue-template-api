#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  OsType.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  OsType 系统类型
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from app.extensions.BaseModel import BaseModel


class OsType(BaseModel):
    __tablename__ = 'os_type'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    name = Column('name', String(50), doc='名字')
    parent_id = Column('parent_id', INTEGER(unsigned=True), ForeignKey('os_type.id'), doc='父Id')
