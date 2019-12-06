#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  __init__.py.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
from celery import Celery
from flask_mail import Mail

from app.app import create_app

SQLALCHEMY_ECHO = True
flask_app = create_app()
mail = Mail(flask_app)
