#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  BaseModel.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  基础Model类
import time
from datetime import datetime

from sqlalchemy import Column, String, Boolean, func, DateTime, desc

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy.dialects.mysql import INTEGER

from app.config.setting import DEFAULT_START_PAGE, DEFAULT_PAGE_SIZE
from app.helper.ModelHelper import model_to_dict
from app.libs.handler.APIException import APIException
from app.enums.ResultEnum import ResultEnum
from app.config.log.LoguruConfig import logger


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 0
        return super(Query, self).filter_by(**kwargs)

    #
    # def filter(self, *args):
    #     return super(Query, self).filter(and_(BaseModel.status == 0, *args))

    def get_or_404(self, ident, description=None):
        rv = self.get(ident)
        if not rv:
            raise APIException(ResultEnum.NOT_FOUND_ERROR)
        return rv

    def first_or_404(self, description=None):
        rv = self.first()
        if not rv:
            raise APIException(ResultEnum.NOT_FOUND_ERROR)
        return rv


db = SQLAlchemy(query_class=Query)


def session_commit():
    try:
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        reason = str(e)
        return reason


class BaseModel(db.Model):
    __abstract__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB'
    }

    id = Column('id', INTEGER(unsigned=True), primary_key=True, autoincrement=True, doc='Id')
    created_time = Column('created_time', DateTime, default=func.now(), doc='创建时间')
    updated_time = Column('updated_time', DateTime, default=func.now(), onupdate=func.now(), doc='更新时间')
    deleted_time = Column('deleted_time', DateTime, default=None, doc='删除时间')
    status = Column('status', Boolean, default=False, doc='删除标记 0 -- 未删除， 1 -- 已删除')
    remark = Column('remark', String(255), doc='备注')
    disabled = Column('disabled', Boolean, default=False, doc='禁用标记 False -- 正常 True -- 已禁用')

    def __getstate__(self):
        return self.as_dict()

    def __setstate__(self, state):
        self.__dict__.update(state)

    @classmethod
    def get_by_status(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get(cls, _id):
        return cls.query.filter(cls.id == _id).first()

    @classmethod
    def get_by_status_or_404(cls, _id):
        return cls.query.filter_by(id=_id).first_or_404()

    @classmethod
    def get_or_404(cls, _id):
        return cls.query.filter(cls.id == _id).first_or_404()

    @classmethod
    def get_all(cls):
        return cls.query.filter(cls.status == 0).all()

    @classmethod
    def get_pagination(cls, start=DEFAULT_START_PAGE, page_size=DEFAULT_PAGE_SIZE, **kwargs):
        result = None

        try:
            result = cls.query.filter_by(**kwargs).order_by(desc(cls.created_time)).paginate(start, page_size,
                                                                                             error_out=False)
        except Exception as e:
            logger.error(e)
        return result

    def delete(self):
        self.deleted_time = datetime.now().isoformat()
        self.status = True
        return session_commit()

    def toggle_disable(self):
        self.disabled = not self.disabled
        return session_commit()

    def save(self, **kwargs):
        for key, value in kwargs.items():
            if key != 'password' and hasattr(self, key):
                setattr(self, key, value)
        db.session.add(self)
        return session_commit()

    def update(self, **kwargs):
        self.updated_time = datetime.now().isoformat()
        for key, value in kwargs.items():
            if key != 'password' and hasattr(self, key) and not isinstance(value, dict):
                setattr(self, key, value)
        return session_commit()

    def as_dict(self, handle_relationship_flag=False):
        return model_to_dict(self, handle_relationship_flag)
