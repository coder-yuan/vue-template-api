#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  UploadSet
# @Author   :  jackeroo
# @Time     :  2019/11/28 9:58 上午
# @File     :  UploadSet.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :
from flask_uploads import UploadSet as _UploadSet, lowercase_ext
from werkzeug.utils import secure_filename

from app.helper.CommonHelper import file_name_to_ascii


class UploadSet(_UploadSet):

    @classmethod
    def secure_filename(cls, filename):
        filename = file_name_to_ascii(filename)
        basename = secure_filename(filename)
        return basename

    def get_basename(self, filename):
        return lowercase_ext(self.secure_filename(filename))
