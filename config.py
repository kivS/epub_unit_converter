'''
    Configs
'''

import logging.config
import textwrap
import os
import warnings

# Report all mistakes managing asynchronous resources.
warnings.simplefilter('always', ResourceWarning)

# SERVER params
# https://aiohttp.readthedocs.io/en/stable/web_reference.html#aiohttp.web.run_app
SERVER = {
    'port': 7000,
}
SERVER['print'] = print(f'''
    ======== Running on http://localhost:{SERVER.get("port", 7000)} ========
                    (Press CTRL+C to quit)
''')


# Logging settings

# create logs folder
if not os.path.exists('logs'):
    os.makedirs('logs')

# allocate 1MB to each log file
MAX_FILE_SIZE_IN_BYTES = 1 * 1024 * 1024

LOGGING = {
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
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        "app_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "formatter": "detailed",
            "maxBytes": MAX_FILE_SIZE_IN_BYTES
        },
        "aiohttp_access_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/aiohttp_access.log",
            "formatter": "detailed",
            "maxBytes": MAX_FILE_SIZE_IN_BYTES
        },
        "aiohttp_web_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/aiohttp_web.log",
            "formatter": "detailed",
            "maxBytes": MAX_FILE_SIZE_IN_BYTES
        },
        "aiohttp_websocket_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/aiohttp_websocket.log",
            "formatter": "detailed",
            "maxBytes": MAX_FILE_SIZE_IN_BYTES
        },
        "asyncio_file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/asyncio.log",
            "formatter": "detailed",
            "maxBytes": MAX_FILE_SIZE_IN_BYTES
        },
    },
    "loggers": {
        "asyncio": {
            "handlers": ["console", "asyncio_file"],
            "level": "DEBUG"
        },
        "aiohttp.access": {
            "level": "DEBUG",
            "handlers": ["console", "aiohttp_access_file"]

        },
        "aiohttp.web": {
            "level": "DEBUG",
            "handlers": ["console", "aiohttp_web_file"]
        },
        "aiohttp.websocket": {
            "level": "DEBUG",
            "handlers": ["console", "aiohttp_websocket_file"]
        },
        "app": {
            "level": "DEBUG",
            "handlers": ["console", "app_file"]
        }
    }
}
# commit logging configs
logging.config.dictConfig(LOGGING)

