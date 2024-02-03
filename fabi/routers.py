#!/usr/bin/env python3

from fastapi import APIRouter
from starlette.requests import Request

import fabi.readers as Readers
from fabi.settings import CACHE_FIXED_SIZE
from fabi.utils.logging_utils import service_logger
from cachetools import LRUCache


api_router = APIRouter()
cache = LRUCache(maxsize=CACHE_FIXED_SIZE)

@api_router.get("/status", status_code=200, tags=["api"])
async def get_user(request: Request):
    return "OK"


@api_router.get("/crawl", status_code=200, tags=["api"])
async def crawl_schema(request: Request):
    cache_items = list(cache.items())
    if cache_items:
        return cache_items

    return Readers.crawl_table_schema()


@api_router.get("/tables", status_code=200, tags=["api"])
async def get_table_names(request: Request):
    table_names = list(cache.keys())
    if table_names:
        return table_names

    return Readers.get_table_names()


@api_router.get("/schema/{tablename}", status_code=200, tags=["api"])
async def get_table_names(tablename: str):
    schema = Readers.get_cache_value(cache, tablename)
    if schema:
        return schema

    return Readers.get_table_schema(tablename)
