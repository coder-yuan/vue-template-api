#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  Cabinet.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  机柜登记类
from sqlalchemy import Column, String
from sqlalchemy.dialects.mssql import TINYINT

from app.extensions.BaseModel import BaseModel


class Cabinet(BaseModel):
    __tablename__ = 'cabinet'
    __table_args__ = {

    }

    code = Column('code', String(30), doc='编号')
    type = Column('type', TINYINT, doc='机柜类型，1为1U，2为2U，0为台式')
    name = Column('name', String(50), doc='机柜名')
