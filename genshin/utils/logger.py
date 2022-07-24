import sys

from loguru import logger

config = {
    # format DOC：https://loguru.readthedocs.io/en/stable/api/logger.html#record
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>",
            "level": "INFO",
            "colorize": True,
        },
        {
            "sink": "log/log_{time:YYYY-MM}.log",
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | {file}:{line} | {function}() | message: {message}",
            "level": "DEBUG",
        },
    ],
}

logger.configure(**config)
