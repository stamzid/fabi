#!/usr/bin/env python3

import os


PUBLIC_SCHEMA_ONLY = os.getenv("PUBLIC_SCHEMA_ONLY", True)
CACHE_FIXED_SIZE = os.getenv("CACHE_FIXED_SIZE", 1000)
CRAWL_INTERVAL = os.getenv("CRAWL_INTERVAL", 30)
