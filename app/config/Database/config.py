#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  setting.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  Database config


class DatabaseBaseConfig:
    DEBUG = True
    REPO = 'db_repository'


class DatabaseProductConfig(DatabaseBaseConfig):
    DEBUG = False

    DataBase = {
        'DB_HOST': '47.102.102.211',
        'DB_PORT': '3306',
        'DB_USER': 'root',
        'DB_PWD': 'All4Xncd',
        'DB_NAME': 'flask_jwt',
        'DB_ECHO': False
    }


class DatabaseDevelopmentConfig(DatabaseBaseConfig):
    DataBase = {
        'DB_HOST': 'ipointek.3322.org',
        'DB_PORT': '3307',
        'DB_USER': 'root',
        'DB_PWD': 'All4Icode',
        'DB_NAME': 'flask_jwt',
        'DB_ECHO': True
    }


class DatabaseTestConfig(DatabaseBaseConfig):
    DataBase = {
        'DB_HOST': 'ipointek.3322.org',
        'DB_PORT': '3307',
        'DB_USER': 'root',
        'DB_PWD': 'All4Icode',
        'DB_NAME': 'flask_jwt',
        'DB_ECHO': True
    }

