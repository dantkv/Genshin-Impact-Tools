from enum import Enum
import os
import sys

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

class UserDataEnum():
    """
    用户数据存储路径枚举
    """
    UID:str = ""
    # 用户数据根目录
    USER_DATA_PATH:str = ""
    # 抽卡记录文件路径
    GACHA_DATA_FILE_PATH:str = ""
    # 统计结果路径
    RESULT_FILE_PATH:str = ""
    # 配置文件路径
    CONFIG_FILE_PATH:str = ""

    def __init__(self, uid) -> None:
        self.update(uid)

    def update(self, uid):
        self.UID= uid
        self.USER_DATA_PATH = os.path.join(CommonEnum.DATA_PATH.value, str(self.UID))
        self.GACHA_DATA_FILE_PATH = os.path.join(self.USER_DATA_PATH, "gacha_data.json")
        self.RESULT_FILE_PATH = os.path.join(self.USER_DATA_PATH, "result.json")
        self.CONFIG_FILE_PATH = os.path.join(self.USER_DATA_PATH, "config.json")

def getUID():
    """
    从游戏文件获取UID
    """
    uid_info_file = os.path.join(CommonEnum.USERPROFILE.value, "AppData", "LocalLow", "miHoYo", "原神", "UidInfo.txt")
    with open(uid_info_file, "r", encoding="utf-8", errors="ignore") as f:
        uid = f.readline().rstrip()
    return uid

USER_DATA_ENUM = UserDataEnum(getUID())