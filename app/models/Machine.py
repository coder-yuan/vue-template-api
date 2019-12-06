#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  Machine.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  主机类
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.dialects.mysql import INTEGER

from app.extensions.BaseModel import BaseModel


class Machine(BaseModel):
    __tablename__ = 'machine'
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    name = Column('name', String(40), doc='主机名')
    code = Column('code', String(40), doc='主机编码')
    machine_type = Column('machine_type', TINYINT, doc='主机类型： 0 --物理主机， 1 - VmWare, 2 -- VPS ')
    parent_id = Column('parent_id', INTEGER(unsigned=True), doc='父主机Id')
    os_last_install_time = Column('os_last_install_time', DateTime, doc='主机系统最后安装时间')
    login_type = Column('login_type', TINYINT, doc='主机登录类型： 0 - ssh user/pass, 1 - ssh/key, 2 - rdp user/pass')
    last_login_user_id = Column('last_login_user_id', INTEGER(unsigned=True), doc='最后登录用户Id')
    last_login_time = Column('last_login_time', DateTime, doc='最后登录时间')
    id_dept = Column('id_dept', INTEGER(unsigned=True), doc='部门Id')
    id_idc = Column('id_idc', INTEGER(unsigned=True), doc='所属Idc的Id')
