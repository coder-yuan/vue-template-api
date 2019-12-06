#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/13
# @File     :  DatetimeHandler.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  jsonpickle序列化Datetime格式定制
from datetime import datetime
import jsonpickle

RFC3339_STRING = '%Y-%m-%dT%H:%M:%S.%fZ'
RFC3339_NO_FRACTION = '%Y-%m-%dT%H:%M:%SZ'
RFC3339_NO_ZULU = '%Y-%m-%dT%H:%M:%S.%f'
RFC3339_NO_FRACTION_NO_ZULU = '%Y-%m-%dT%H:%M:%S'
RFC3339_STRING_DATE_ONLY = '%Y-%m-%d'
RFC3339_DEFAULT = '%Y-%m-%d %H:%M:%S'
VALID_TIMESTAMP_KEYS = ('datetime', 'date', 'timestamp')

VALID_DATETIME_STRINGS = [
    RFC3339_STRING, RFC3339_NO_FRACTION, RFC3339_NO_ZULU, RFC3339_NO_FRACTION_NO_ZULU
]


class DatetimeHandler(jsonpickle.handlers.BaseHandler):

    def restore(self, obj):
        pass

    def flatten(self, obj: datetime, data):
        return obj.strftime(RFC3339_DEFAULT)
