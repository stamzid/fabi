#!/usr/bin/env python3

import fabi.db_access as DBA
import fabi.db_queries as Queries

from cachetools import LRUCache
from collections import defaultdict
from fabi.settings import PUBLIC_SCHEMA_ONLY


def set_cache_value(cache: LRUCache, key: str, value: dict):
    cache[key] = value


def get_cache_value(cache: LRUCache, key: str):
    return cache.get(key, None)


def get_query(key: str):
    if PUBLIC_SCHEMA_ONLY:
        return Queries.public_queries[key]

    return Queries.all_queries[key]


def crawl_table_schema():
    query = get_query("crawl")

    return_data = defaultdict(list)
    count, data = DBA.execute_read_without_condition(query)
    if count == 0:
        return {}

    for row in data:
        column_metadata = {
            "column_name": row["column_name"],
            "data_type": row["data_type"],
            "is_nullable": row["is_nullable"],
            "column_default": row["column_default"]
        }
        return_data[row["table_name"]].append(column_metadata)

    return return_data


def get_table_names():
    query = get_query("tables")
    count, data = DBA.execute_read_without_condition(query)
    if count == 0:
        return []

    return [row["table_name"] for row in data]


def get_table_schema(tablename: str):
    query = Queries.get_table_schema
    record = (tablename,)
    count, data = DBA.execute_read_query(query, record)
    if count == 0:
        return []

    return data
