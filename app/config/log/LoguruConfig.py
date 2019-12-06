#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/13
# @File     :  LoguruConfig.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
import sys

from loguru import logger

# 每周一个日志文件
LOGURU_ROTATION = '1 week'

# 最多保留300天
LOGURU_RETENTION = '300 days'

# 压缩格式
LOGURU_COMPRESS = 'zip'

LOGURU_FILE_LEVEL = 'INFO'
LOGURU_CONSOLE_LEVEL = 'DEBUG'

# remove default logger
logger.remove()

# add file logger
logger.add('logs/fws_{time}.log', rotation=LOGURU_ROTATION,
           retention=LOGURU_RETENTION,
           compression=LOGURU_COMPRESS,
           level=LOGURU_FILE_LEVEL)

# add console logger
logger.add(sys.stdout, level=LOGURU_CONSOLE_LEVEL)
