'''
    Configs
'''

import logging.config
import textwrap
import os
from typing import List, Dict
import argparse


CLIENT_DEV_ADDR = 'http://localhost:8080/'

# SERVER params
# https://aiohttp.readthedocs.io/en/stable/web_reference.html#aiohttp.web.run_app
SERVER = {
    'port': 7000,
    'host': '127.0.0.1',
    'print': None
}


# Logging settings
#
# create logs folder
if not os.path.exists('logs'):
    os.makedirs('logs')

# allocate 1MB to each log file
MAX_FILE_SIZE_IN_BYTES = 1 * 1024 * 1024

LOGGING: Dict = {
    "version": 1,
    "disable_existing_loggers": "True",
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s \n",
            "datefmt": "%d-%m-%Y %I:%M:%S %p"
        },
        "detailed": {
            "format": textwrap.dedent('''
            TIME: %(asctime)s
            NAME: %(name)s
            LEVEL: %(levelname)s
            FILENAME: %(filename)s - line %(lineno)d

            %(message)s
            ---
            '''),
            "datefmt": "%d-%m-%Y %I:%M:%S %p"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        "app_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "formatter": "detailed",
            "maxBytes": MAX_FILE_SIZE_IN_BYTES
        },
        "aiohttp_access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/aiohttp_access.log",
            "formatter": "detailed",
            "maxBytes": MAX_FILE_SIZE_IN_BYTES
        },
        "aiohttp_web_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/aiohttp_web.log",
            "formatter": "detailed",
            "maxBytes": MAX_FILE_SIZE_IN_BYTES
        },
        "aiohttp_websocket_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/aiohttp_websocket.log",
            "formatter": "detailed",
            "maxBytes": MAX_FILE_SIZE_IN_BYTES
        },
        "asyncio_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/asyncio.log",
            "formatter": "detailed",
            "maxBytes": MAX_FILE_SIZE_IN_BYTES
        },
    },
    "loggers": {
        "asyncio": {
            "handlers": ["console", "asyncio_file"],
            "level": "ERROR"
        },
        "aiohttp.access": {
            "level": "ERROR",
            "handlers": ["console", "aiohttp_access_file"]

        },
        "aiohttp.web": {
            "level": "ERROR",
            "handlers": ["console", "aiohttp_web_file"]
        },
        "aiohttp.websocket": {
            "level": "ERROR",
            "handlers": ["console", "aiohttp_websocket_file"]
        },
        "app": {
            "level": "ERROR",
            "handlers": ["console", "app_file"]
        }
    }
}
# commit logging configs
logging.config.dictConfig(LOGGING)


# File extensions inside EPUB files that are targeted for conversion
ALLOWED_EPUB_CONTENT_FILE_EXTENSIONS: List[str] = ['html', 'xhtml']


# Arguments parser
# define the parser
ARGS_PARSER = argparse.ArgumentParser(
    description='Epub Unit Converter'
)
# add arguments
ARGS_PARSER.add_argument(
    '-d', '--dev',
    dest='dev',
    help='Activate dev mode',
    default=False,
    action='store_true'
)
ARGS_PARSER.add_argument(
    '-rl', '--rm-logs',
    dest='rm_logs',
    help='Resets the logs',
    default=False,
    action='store_true'
)
