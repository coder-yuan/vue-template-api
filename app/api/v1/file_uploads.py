#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  flask_file_upload
# @Author   :  jackeroo
# @Time     :  2019/11/27 6:23 下午
# @File     :  file_uploads.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_uploads import IMAGES

from app.domain.UploadSet import UploadSet
from app.enums.ResultEnum import ResultEnum
from app.helper.HttpHelper import HttpHelper
from app.libs.handler.APIException import APIException
from app.libs.redprint import RedPrint
from app.models.SysFile import SysFile

api = RedPrint('file_uploads')
avatar = UploadSet('avatar', extensions=IMAGES)


@api.route('', methods=['POST'])
@jwt_required
def upload():
    if 'avatar' not in request.files:
        raise APIException(ResultEnum.FILE_UPLOAD_METHOD_ERROR)

    file = request.files['avatar']
    org_name = file.filename

    # 调用Flask-uploads进行存储
    # 1、目标路径不存在自动创建
    # 2、重名自动加自增的数字后缀
    # 3、根据配置的允许后缀或者拒绝后缀进行过滤
    filename = avatar.save(file)
    url = avatar.url(filename)

    # 入库
    current_user = get_jwt_identity()
    _avatar = SysFile(file_name=filename, org_name=org_name, operator_id=current_user.get('id'), file_url=url)
    _avatar.save()

    return HttpHelper.normal_handler(_avatar)
