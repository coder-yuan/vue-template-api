#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  SysFile
# @Author   :  jackeroo
# @Time     :  2019/11/27 10:14 上午
# @File     :  SysFile.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :  文件管理
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.mysql import INTEGER

from app.extensions.BaseModel import BaseModel


class SysFile(BaseModel):
    __tablename__ = 'sys_file'

    org_name = Column('org_name', String(255), doc='原始文件名')
    file_name = Column('file_name', String(255), nullable=False, doc='文件名')
    file_path = Column('file_path', String(255), doc='文件路径')
    file_url = Column('file_url', String(255), doc='文件URL')
    file_type = Column('file_type', Integer(), default=0, doc='文件类型：目前无业务需求，默认为0')
    operator_id = Column('operator_id', INTEGER(unsigned=True), default=None, doc='上传用户的Id')

    def upload(self):
        pass

    def download(self):
        pass
