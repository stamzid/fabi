#!/usr/bin/env python3

import logging

service_logger = logging.getLogger('fabi-client')
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('fabi-client.log', mode='w')
formatter = logging.Formatter('%(levelname)s: %(asctime)s %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

service_logger.setLevel(logging.INFO)
service_logger.addHandler(file_handler)
service_logger.addHandler(console_handler)
