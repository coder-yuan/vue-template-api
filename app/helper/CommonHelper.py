#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project  :  icode_flask_be
# @Package  :  
# @Author   :  jackeroo
# @Time     :  2019/11/23 上午10:12
# @File     :  CommonHelper.py
# @Contact  :  
# @Software :  PyCharm
# @Desc     :
import uuid

from pypinyin import lazy_pinyin


def get_accurated_dict(key_words, **kwargs):
    """
    处理字典
    1、 返回关键key列表中的非空部分acc_ret
    2、 同时返回其余非空部分kw_ret"""
    acc_ret = dict()
    kw_ret = dict()

    for (key, value) in kwargs.items():

        if value is None:
            continue

        if key in key_words:
            acc_ret[key] = value
        else:
            kw_ret[key] = value

    return acc_ret, kw_ret


def get_uuid_file_name(file_name):
    """通过UUID生成不重复的文件名"""
    if not file_name:
        return ''

    filename = uuid.uuid4().hex
    file_ext = file_name.split('.')[-1]

    if file_ext:
        filename = filename + '.' + file_ext

    return filename


def is_contain_chinese(check_str):
    """判断字符串中是否包括有汉字"""
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


def file_name_to_ascii(filename):
    """
    如果是汉字，转化为拼音文件名
    :param filename:
    :return:
    """
    f_name = filename.split('.')
    name = list()
    for n in f_name[:-1]:
        if is_contain_chinese(n):
            name += lazy_pinyin(n)
        else:
            name.append(n)

    return '_'.join(name) + '.' + f_name[-1]
