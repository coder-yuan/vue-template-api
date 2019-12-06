#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  setting.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
import datetime

from celery.schedules import crontab

ENV = 'DEVELOPMENT'
if ENV == 'DEVELOPMENT':
    from app.config.Database.config import DatabaseDevelopmentConfig as DbConfig
elif ENV == 'PRODUCTION':
    from app.config.Database.config import DatabaseProductConfig as DbConfig
else:
    from app.config.Database.config import DatabaseTestConfig as DbConfig

# 分页展示插件默认参数
DEFAULT_START_PAGE = 1
DEFAULT_PAGE_SIZE = 20

# 文件上传配置
UPLOADS_DEFAULT_DEST = 'app/static/images'
UPLOADS_DEFAULT_URL = '/images/'
FILE_UPLOAD_ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Flask App监听IP和端口
DEBUG = True
HOST = '0.0.0.0'
PORT = 9000
SECRET_KEY = '\xd7l\xca\x8e\x91e\xc9\x8c\xb2\x03r\xd7\xe6\xc1\xe8\x9e\x04^\xd16\xd7|\xeaz'
BASE_URL = 'http://192.168.0.117:9000/'

# SqlAlchemy configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s' % (DbConfig.DataBase['DB_USER'],
                                                              DbConfig.DataBase['DB_PWD'],
                                                              DbConfig.DataBase['DB_HOST'],
                                                              DbConfig.DataBase['DB_PORT'],
                                                              DbConfig.DataBase['DB_NAME'])

# IF JWT_SECRET_KEY not set, it will use the flask app's secret key
JWT_AUTH_URL_RULE = '/login'
JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)

######################################################
# Celery配置项                                        #
######################################################
CELERY_RESULT_BACKEND = 'redis://:All4Icode@localhost:6379/0'
BROKER_URL = 'redis://:All4Icode@localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Chongqing'
CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS = {'visibility_timeout': 18000}
# result_backend_transport_options ={'visibility_timeout': 18000}
# CELERY_IMPORTS = ('app.tasks.workers',)
CELERYBEAT_SCHEDULE = {
    'add-every-1-min': {
        'task': 'app.tasks.tasks.add_together',
        'schedule': crontab(),
        'args': (16, 16),
    },
}

# Flask-Mail 配置
MAIL_SERVER = 'http://localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = 'jackeroo@qq.com'
MAIL_MAX_EMAILS = None
MAIL_SUPPRESS_SEND = True
MAIL_ASCII_ATTACHMENTS = False

# 用户级别配置
ACCESS = {
    'guest': 0,
    'user': 1,
    'super_admin': 99
}
