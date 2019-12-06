#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   :  jackeroo
# @Time     :  2019/11/10
# @File     :  HttpHelper.py
# @Contact  :  jackeroo@qq.com
# @Software :  PyCharm
# @Desc     :  Http访问工具类
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from app.config.json.Json import jsonpickle
from app.config.log.LoguruConfig import logger
from flask import Response, request

from app.enums.ResultEnum import ResultEnum
from app.helper.ResultHelper import ResultHelper


class HttpHelper:
    class BearerAuth(requests.auth.AuthBase):
        def __init__(self, token=None):
            self.token = token

        def __call__(self, r):
            r.headers['Authorization'] = 'Bearer {}'.format(self.token)
            return r

    @staticmethod
    def http_basic_auth(auth_url, username, password):
        if not (auth_url and username and password):
            raise ValueError(
                "When authentication, username and password and authUrl"
                "must be provided"
            )
        return requests.get(auth_url, auth=HTTPBasicAuth(username, password))

    @staticmethod
    def http_digest_auth(auth_url, username, password):
        if not (auth_url and username and password):
            raise ValueError(
                "When authentication, username and password and authUrl"
                "must be provided"
            )
        return requests.get(auth_url, auth=HTTPDigestAuth(username, password))

    @staticmethod
    def get_auth_token_by_type(auth_type, auth_token):
        if auth_type == 'Bearer':
            token = HttpHelper.BearerAuth(auth_token)()
        elif auth_type == 'OAuth2':
            token = None
        else:
            token = None

        return token

    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)

        # 异常判定
        if r.status_code != 200:
            return {} if return_json else ''

        # 正常业务数据返回
        return r.json() if return_json else r.text

    @staticmethod
    def token_get(url, auth_token, return_json=True):
        r = requests.get(url, auth=HttpHelper.BearerAuth(auth_token))

        if r.status_code != 200:
            return {} if return_json else ''

        return r.json() if return_json else r.text

    @staticmethod
    def post(url, data=None, auth_token=None, return_json=True, auth_type='Bearer'):
        if auth_token:
            token = HttpHelper.get_auth_token_by_type(auth_type, auth_token)
            try:
                r = requests.post(url, json=data, auth_token=token)
            except Exception as e:
                logger.error(e)
                return HttpHelper.error_handler(ResultEnum.UNKNOWN_ERROR)
        else:
            try:
                r = requests.post(url, json=data)
            except Exception as e:
                logger.error(e)
                return HttpHelper.error_handler(ResultEnum.UNKNOWN_ERROR)

        return r.json() if return_json else r.text()

    @staticmethod
    def json_response(result, response_status=200):
        ret = {
            'error_code': result.error_code,
            'msg': result.msg,
            'success': result.success,
            'data': result.data
        }
        content = jsonpickle.encode(ret, unpicklable=False, max_depth=20)
        resp = Response(
            content,
            mimetype='application/json'
        )
        logger.debug('Http response: ( {},  {}'.format(result.code, content))
        return resp, result.code

    @staticmethod
    def normal_handler(data=None):
        return HttpHelper.json_response(ResultHelper.success(data))

    @staticmethod
    def error_handler(result_enum, data=None, resp_status=200):
        logger.error(result_enum)
        return HttpHelper.json_response(ResultHelper.error_with_enum(result_enum, data), resp_status)

    @staticmethod
    def get_page_info():
        start = request.args.get('start', default=0, type=int)
        pagesize = request.args.get('pagesize', default=20, type=int)
        return start, pagesize


if __name__ == '__main__':
    base_url = 'http://127.0.0.1:9999'
    login_url = base_url + '/login'
    reg_url = base_url + '/register'
    user = {'username': 'jackeroo', 'password': '2345678'}
    login_info = HttpHelper.post(login_url, data=user)
    logger.debug(login_info)
    if login_info.get('code') == 200:
        logger.debug(login_info.get('data'))
    else:
        logger.debug('Error: code {} msg: {}'.format(login_info.get('code'), login_info.get('msg')))
