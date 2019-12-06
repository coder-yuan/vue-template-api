#!/usr/bin/env python3

from enum import Enum
from collections import namedtuple

ResultEnums = namedtuple('Result', ['code', 'error_code', 'msg'])


class ResultEnum(Enum):

    @property
    def msg(self):
        return self.value.msg

    @property
    def code(self):
        return self.value.code

    @property
    def error_code(self):
        return self.value.error_code

    @staticmethod
    def get_enum_by_code(_code):
        for key, item in ResultEnum.__members__.items():
            if item.code == _code:
                return item
        return ResultEnum.UNKNOWN_ERROR

    @staticmethod
    def get_enum_by_error_code(_error_code):
        for key, item in ResultEnum.__members__.items():
            if item.error_code == _error_code:
                return item
        return ResultEnum.UNKNOWN_ERROR

    # 通用
    SUCCESS = ResultEnums(200, 200, "成功")
    INSERT_SUCCESS = ResultEnums(200, 201, '新增成功')
    DELETE_SUCCESS = ResultEnums(200, 204, '删除成功')
    INVALID_PARAMETER = ResultEnums(200, 500400, "无效参数")
    ACCESS_FORBIDDEN = ResultEnums(200, 400403, '拒绝访问')
    UNKNOWN_ERROR = ResultEnums(200, 500205, "未知错误")

    # User相关相关
    USER_NOT_FOUND_ERROR = ResultEnums(200, 500402, '用户不存在')
    USER_PASSWORD_ERROR = ResultEnums(200, 500403, '用户密码错误')
    USER_OR_PASS_EMPTY_ERROR = ResultEnums(200, 9500404, '用户名和密码不能为空')
    USER_REGISTER_ERROR = ResultEnums(200, 900405, '用户注册失败')
    USER_ALREADY_EXIST_ERROR = ResultEnums(200, 900406, '用户已存在')
    USER_DELETE_ERROR = ResultEnums(200, 900407, '用户删除失败')
    USER_UPDATE_ERROR = ResultEnums(200, 900408, '用户更新失败')
    USER_INVALID_ID = ResultEnums(200, 900409, '用户Id错误')

    # Token相关操作
    TOKEN_VALIDATE_ERROR = ResultEnums(200, 400401, 'Token身份验证失败')
    TOKEN_EXPIRED_ERROR = ResultEnums(200, 400402, 'Token已失效')
    TOKEN_INVALID_FORMAT = ResultEnums(200, 400403, '非法Token格式')

    # Role相关
    ROLE_INVALID_ID = ResultEnums(200, 400404, 'RoleID错误')
    ROLE_CODE_EXIST = ResultEnums(200, 400405, '角色code已存在')

    # Permission相关
    PERMISSION_INVALID_ID = ResultEnums(200, 400404, 'PermissionID错误')
    PERMISSION_EMPTY_CODE = ResultEnums(200, 400405, 'Permission code不能为空')
    PERMISSION_CODE_EXISTS = ResultEnums(200, 400406, 'Permission code已存在')

    # misc
    NOT_FOUND_ERROR = ResultEnums(200, 500404, '资源找不到')
    PAGE_NOT_FOUND_ERROR = ResultEnums(200, 400404, '页面找不到')
    METHOD_NOT_ALLOWED_ERROR = ResultEnums(200, 400405, '请求Method不允许')
    JSON_SCHEMA_VALIDATION_ERROR = ResultEnums(200, 500206, 'Json校验失败')

    # 文件操作
    FILE_UPLOAD_ERROR = ResultEnums(200, 500301, '文件上传失败')
    FILE_NOT_ALLOWED_EXTENSION = ResultEnums(200, 500302, '文件后缀不允许')
    FILE_NOT_EXIST_ERROR = ResultEnums(200, 500303, '文件没找到')
    FILE_UPLOAD_METHOD_ERROR = ResultEnums(200, 500304, '文件参数必须为file或者files（多文件上传）')


if __name__ == '__main__':
    code = 200
    print(ResultEnum.get_enum_by_error_code(ResultEnum.INVALID_PARAMETER.error_code))
