#!/usr/bin/env python3

import redis

from fabi.settings import REDIS_HOST, REDIS_PORT

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=0)


def redis_conn():
    return redis.Redis(connection_pool=pool)
