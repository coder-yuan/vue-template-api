#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/15
# @File     :  client.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  根据客户端不同，分别进行不同的方式注册
from flask import request
from werkzeug.security import generate_password_hash

from app.config.log.LoguruConfig import logger

from app.enums.ClientTypeEnum import ClientTypeEnum
from app.enums.ResultEnum import ResultEnum
from app.helper.HttpHelper import HttpHelper
from app.libs.handler.APIException import APIException
from app.libs.redprint import RedPrint
from app.models.User import User
from app.validators.client.ClientRegisterValidator import ClientRegisterValidator

api = RedPrint('client')


@api.route('/register', methods=['POST'])
def register_client():
    reg_info = ClientRegisterValidator.validator(request.json)

    promise = {
        ClientTypeEnum.USER_EMAIL.code: __register_by_email,
        ClientTypeEnum.USER_MOBILE.code: __register_by_mobile,
        ClientTypeEnum.USER_MINA.code: __register_by_mina,
        ClientTypeEnum.USER_WECHAT.code: __register_by_wechat
    }

    reg_type = reg_info.get('clientType')
    client = promise[reg_type](reg_info.get('account'), reg_info.get('password'))
    return HttpHelper.normal_handler(client)


def __register_by_email(account, password):
    try:
        client_type = ClientTypeEnum.USER_EMAIL.code
        user = User(account=account, password=generate_password_hash(password), client_type=client_type)
        user.save()
        return user
    except Exception as e:
        logger.error(e)
        if isinstance(e, APIException):
            ret = e.result_enum
        else:
            ret = ResultEnum.USER_REGISTER_ERROR
        raise APIException(ret)


def __register_by_mobile():
    pass


def __register_by_mina():
    pass


def __register_by_wechat():
    pass
