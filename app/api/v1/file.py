#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  file
# @Author   :  jackeroo
# @Time     :  2019/11/27 10:31 上午
# @File     :  file.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :  文件处理
import os

from flask import request
from flask_jwt_extended import jwt_required

from app.config.setting import FILE_UPLOAD_ALLOWED_EXTENSIONS, UPLOADS_DEFAULT_DEST
from app.enums.ResultEnum import ResultEnum
from app.helper import CommonHelper
from app.helper.HttpHelper import HttpHelper
from app.libs.handler.APIException import APIException
from app.libs.redprint import RedPrint
from app.config.log.LoguruConfig import logger
from app.extensions.BaseModel import session_commit
from app.models.SysFile import SysFile

api = RedPrint('file')


def allowed_file(filename):
    file_ext = filename.split('.')[-1]
    if file_ext and file_ext.lower() in FILE_UPLOAD_ALLOWED_EXTENSIONS:
        return True
    return False


@api.route('', methods=['POST'])
@jwt_required
def file_upload():
    """
    文件上传，支持单文件和多文件
    1、 单文件上传，body中必须以file指定文件
    2、 多文件上传，body中必须以files指定文件列表
    :return:  成功、错误 json文件
    """

    # 如果是通过file关键字进行的文件上传，即使多个也只处理最后一个
    if 'file' in request.files:

        file = request.files.get('file')
        if file:
            succ, data = process_single_file(file)
            if succ:
                return HttpHelper.normal_handler(data)
            else:
                return HttpHelper.error_handler(data)

    else:
        errors = {}
        success = {}
        files = request.files.getlist('files')

        # 不是file，也不是files参数，抛异常退出
        if not files:
            raise APIException(ResultEnum.FILE_UPLOAD_METHOD_ERROR)

        for file in files:
            succ, data = process_single_file(file)
            if succ:
                success[file.filename] = data
            else:
                errors[file.filename] = data.msg

        data = {
            'success': success,
            'errors': errors
        }
        return HttpHelper.normal_handler(data)


def process_single_file(file):
    success = False
    if file and allowed_file(file.filename):
        file_path = None

        try:
            org_file_name = file.filename

            file_name = CommonHelper.get_uuid_file_name(org_file_name)
            file_path = os.path.join(UPLOADS_DEFAULT_DEST, file_name)

            if not os.path.exists(UPLOADS_DEFAULT_DEST):
                os.mkdir(UPLOADS_DEFAULT_DEST)
            file.save(file_path)

            ret_file = SysFile(file_name=file_name, org_name=org_file_name)
            ret_file.save()
            session_commit()

            success = True
            data = {
                'id': ret_file.id,
                'filename': ret_file.file_name
            }

        except Exception as e:
            logger.error('file save error: {}, {}'.format(file_path, e.args))
            data = ResultEnum.FILE_UPLOAD_ERROR

    else:
        data = ResultEnum.FILE_NOT_ALLOWED_EXTENSION

    return success, data
