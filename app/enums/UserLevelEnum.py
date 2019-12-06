#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/15
# @File     :  ClientTypeEnum.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
from enum import Enum

from app.enums.BaseEnum import BaseEnum


class UserLevelEnum(BaseEnum):
    # 受限用户
    RESTRICTED = 100

    # Email用户
    NORMAL = 1

    # 手机用户
    ADMIN = 50

    # 微信用户
    SUPER_ADMIN = 99

    DEFAULT = NORMAL
