import sys
import platform
import traceback
from loguru import logger
from functools import wraps

config = {
    # format DOC：https://loguru.readthedocs.io/en/stable/api/logger.html#record
    "handlers": [
        {
            "sink": sys.stdout, 
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{message}</level>", 
            "level": "INFO", 
            "colorize": True
        },
        {
            "sink": "log/log_{time:YYYY-MM}.log", 
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | {level} | {file}:{line} | {function}() | message:   {message}", 
            "level":"DEBUG"
        },
    ],
}

logger.configure(**config)
def pressAnyKeyToExit(msg="执行结束，按任意键退出"):
    logger.info(msg)
    try:
        if platform.system() == "Windows":
            from msvcrt import getch
            getch()
        else:
            input()
    except KeyboardInterrupt:
        exit()
    except Exception:
        logger.debug(traceback.format_exc())
    exit()

def catchException(message:str="执行出错", level="error"):
    def callFunction(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception:
                if level == "error":
                    logger.error(message)
                elif level == "info":
                    logger.info(message)
                elif level == "warning":
                    logger.warning(message)
                else:
                    logger.debug(message)
                logger.debug(traceback.format_exc())
                return False
            return result
        return decorated
    return callFunction