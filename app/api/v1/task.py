#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  task
# @Author   :  jackeroo
# @Time     :  2019/11/29 5:25 下午
# @File     :  task.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :
from app.extensions import celery
from flask_jwt_extended import jwt_required

from app.helper.HttpHelper import HttpHelper
from app.libs.redprint import RedPrint

api = RedPrint('task')


@api.route('/<task_id>', methods=['GET'])
@jwt_required
def get_task_result(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return HttpHelper.normal_handler(response)
