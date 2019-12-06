#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  
# @Author   :  jackeroo
# @Time     :  2019/11/21 上午6:47
# @File     :  RedisCache.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :
from flask_caching import Cache
from app.config.Cache.RedisCache import RedisCache

cache = Cache(config=RedisCache)
