import os
import sys
from enum import Enum


class CommonEnum(Enum):
    """
    常量枚举
    """

    ROOT_PATH = os.getcwd()
    # 数据文件根路径
    DATA_PATH = os.path.join(ROOT_PATH, "data")
    # 临时文件路径
    TEMP_PATH = os.path.join(ROOT_PATH, "tmp")
    # 资源文件路径 单文件程序会先解压到临时目录再运行，因此os.getcwd()和资源文件不是一个目录
    RESOURCE_FILE_PATH = os.path.join(getattr(sys, "_MEIPASS", ROOT_PATH), "resource")
    # 系统用户变量
    USERPROFILE = os.environ["USERPROFILE"]
