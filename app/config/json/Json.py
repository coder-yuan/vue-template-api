#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/13
# @File     :  Json.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
from datetime import datetime

import jsonpickle

from app.helper.DatetimeHandler import DatetimeHandler

jsonpickle.set_preferred_backend('simplejson')
jsonpickle.set_encoder_options('simplejson',
                               ensure_ascii=False,  # 中文显示支持
                               sort_keys=True,  # 按照键值排序
                               indent=None,  # 不缩进美化
                               separators=(',', ':')  # 分隔符配置——可以消除键值和键之间的空格
                               )
jsonpickle.handlers.register(datetime, DatetimeHandler)  # 自定义时间显示格式
