#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/16
# @File     :  __init__.py.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  
from flask import Blueprint

error_handler_blueprint = Blueprint('error_handler_blueprint', __name__)

from app.libs.handler import GlobalExceptionHandler
