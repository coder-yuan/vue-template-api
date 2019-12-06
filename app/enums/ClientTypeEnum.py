#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/15
# @File     :  ClientTypeEnum.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :

from app.enums.BaseEnum import BaseEnum


class ClientTypeEnum(BaseEnum):
    # Normal一般用户
    USER_NORMAL = 100

    # Email用户
    USER_EMAIL = 101

    # 手机用户
    USER_MOBILE = 102

    # 微信用户
    USER_WECHAT = 200

    # Mina用户
    USER_MINA = 201

    # 其他用户
    USER_MISC = 300

    DEFAULT = USER_NORMAL
