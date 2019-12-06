from http.client import HTTPException

from flask_json_schema import JsonValidationError

from app.config.log.LoguruConfig import logger
from app.enums.ResultEnum import ResultEnum

from . import error_handler_blueprint
from .APIException import APIException


def http_to_api_exception(e):
    code = e.code
    error_code = 1007
    msg = e.description
    api_exception = APIException(code=code, error_code=error_code, msg=msg)
    return api_exception


@error_handler_blueprint.app_errorhandler(Exception)
def global_error_handler(e):
    if isinstance(e, APIException):
        api_exception = e

    elif isinstance(e, HTTPException):
        api_exception = http_to_api_exception(e)

    elif isinstance(e, JsonValidationError):
        api_exception = APIException(ResultEnum.JSON_SCHEMA_VALIDATION_ERROR, e.message)

    else:
        logger.error(e)
        code = error_code = e.code if hasattr(e, 'code') else 500

        if hasattr(e, 'description'):
            msg = e.description
        elif hasattr(e, 'args'):
            msg = e.args[0]
        else:
            msg = 'unknown error'

        api_exception = APIException(code=code, error_code=error_code, msg=msg)

    logger.debug(
        'code: {}, error_code: {}, msg: {} )'.format(api_exception.code, api_exception.error_code, api_exception.msg))
    return api_exception
