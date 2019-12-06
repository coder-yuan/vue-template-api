#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  FlaskCelery
# @Author   :  jackeroo
# @Time     :  2019/12/1 11:16 上午
# @File     :  FlaskCelery.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :
import flask
from celery import Celery


class FlaskCelery(Celery):

    def __init__(self, app=None, *args, **kwargs):
        self.app = app
        super(FlaskCelery, self).__init__(*args, **kwargs)
        self.patch_task()

        if app:
            self.init_app(app)

    def patch_task(self):
        TaskBase = self.Task
        _celery = self

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                if flask.has_app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                else:
                    with _celery.app.app_context():
                        return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask

    def init_app(self, app):
        self.app = app
        self.config_from_object(app.config)
