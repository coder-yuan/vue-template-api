#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  app
# @Author   :  jackeroo
# @Time     :  2019/11/29 2:45 下午
# @File     :  app.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :

from flask import Flask
from flask_cors import CORS
from flask_uploads import configure_uploads

from app.auth.jwt_authz.JwtAuth import jwt
from app.cache.RedisCache import cache
from app.extensions import celery, db


def _register_blueprint(application):
    from app.libs.handler import error_handler_blueprint
    application.register_blueprint(error_handler_blueprint)

    from app.api import api_blueprint_v1
    application.register_blueprint(api_blueprint_v1, url_prefix='/api/v1')


def init_extensions(application):
    # 配置Celery
    celery.config_from_object('app.config.setting', force=True)
    celery.autodiscover_tasks(['app.task.workers'])
    celery.init_app(application)

    # 数据库连接初始化
    db.init_app(application)
    with application.app_context():
        db.create_all()

    # 配置cache
    cache.init_app(app=application)

    # 配置文件上传
    from app.api.v1.file_uploads import avatar
    configure_uploads(application, (avatar,))

    # JWT Token身份验证初始化
    jwt.init_app(application)


def create_app():
    application = Flask(__name__, static_folder='static/', static_url_path='')
    application.config.from_object('app.config.setting')

    # 注册模块
    _register_blueprint(application)

    # 跨域访问支持，因为我们采用token进行身份验证，所以允许访问所有目录
    CORS(application, resources=r'/*')

    # 配置其他扩展，数据库支持，Celery Task支持、文件上传支持
    init_extensions(application)

    return application
