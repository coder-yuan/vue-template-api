#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/13
# @File     :  workers.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :
from flask import current_app
from flask_mail import Message
from app.app import celery

from app.models.User import User


@celery.task
def add_together(a, b):
    return a + b


@celery.task
def do_something():
    current_app.logger.info('already')


@celery.task
def send_welcome_email(email, user_id, confirmation_link):
    """Background task to send a welcome email with flask-security's mail.
    You don't need to use with app.app_context() as Task has app context.
    """

    from app import mail
    user = User.get_by_status_or_404(user_id)
    print(f'sending user {user.account}: {user.email} a welcome email')

    msg = Message(email, recipients=[user.email])
    msg.body = confirmation_link
    mail.send(msg)


if __name__ == '__main__':
    # result = add_together.delay(23, 42)
    # result.wait()
    #
    # result = send_welcome_email('hi', 9, 'http://localhost:9000/')
    # result.wait()

    result = do_something()
    result.wait()
