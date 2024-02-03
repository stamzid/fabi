#!/usr/bin/env python3

from fastapi import FastAPI
from fabi.routers import api_router, cache
from fabi.settings import CRAWL_INTERVAL
from fabi.readers import crawl_table_schema
from fabi.utils.logging_utils import service_logger

import threading
import time


server = FastAPI()

server.include_router(
    api_router,
    prefix="/api",
    tags=["api"],
    responses={404: {
        "description": "Page Not found"
    }}
)


def crawl_schema_periodically(interval):
    while True:
        service_logger.info("Crawling DB schema...")
        data = crawl_table_schema()
        for key, value in data.items():
            cache[key] = value
        time.sleep(interval)


# Start the background thread
thread = threading.Thread(target=crawl_schema_periodically, args=(CRAWL_INTERVAL,))
thread.daemon = True
thread.start()
