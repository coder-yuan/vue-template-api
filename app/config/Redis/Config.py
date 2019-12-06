#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created by jackeroo at 2019-01-31


class RedisBaseConfig:
    DEBUG = True


class RedisProductConfig(RedisBaseConfig):
    DEBUG = True

    RedisDB = {
        'RedisHost': '47.102.102.211',
        'RedisPort': 6379,
        'RedisPass': 'All4Xncd',
        'RedisDb': 10
    }


class RedisDevelopmentConfig(RedisBaseConfig):
    DEBUG = True

    RedisDB = {
        'RedisHost': 'ipointek.3322.org',
        'RedisPort': 6379,
        'RedisPass': '',
        'RedisDb': 10
    }


class RedisTestConfig(RedisBaseConfig):
    DEBUG = True

    RedisDB = {
        'RedisHost': 'ipointek.3322.org',
        'RedisPort': 6379,
        'RedisPass': 'All4Icode',
        'RedisDb': 10
    }
