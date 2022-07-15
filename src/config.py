from enum import Enum
import json
import os
from utils import catchException
from common import CommonEnum
from utils import logger


class BaseConfig(object):
    """
    配置工具类
    """
    def __init__(self, root_path="data") -> None:
        self.setting = dict()
        self.path = os.path.join(CommonEnum.ROOT_PATH.value, root_path)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
    
    def read(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self.setting.update(json.loads(f.read()))

    def setKey(self, key, value=None):
        self.setting[key] = value
        self.save()

    def getKey(self, key):
        try:
            return self.setting[key]
        except KeyError:
            return None

    def delKey(self, key):
        try:
            del self.setting[key]
        except KeyError:
            pass
        self.save()
    
    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(json.dumps(self.setting, sort_keys=True, indent=4, separators=(",", ":")))


class GlobalConfigEnum(Enum):
    """
    设置项枚举类
    """
    FLAG_SHOW_REPORT = "FLAG_SHOW_REPORT"
    FLAG_CHECK_UPDATE = "FLAG_CHECK_UPDATE"
    FLAG_WRITE_TXT = "FLAG_WRITE_TXT"
    FLAG_WRITE_XLSX = "FLAG_WRITE_XLSX"
    FLAG_USE_CONFIG_URL = "FLAG_USE_CONFIG_URL"
    FLAG_USE_LOG_URL = "FLAG_USE_LOG_URL"


class GlobalConfig(BaseConfig):
    """
    全局配置类
    """

    def __init__(self, config_file_name="config.json"):
        super().__init__()
        self.path = os.path.join(self.path, config_file_name)
        self.setting = {
            # 显示抽卡报告
            GlobalConfigEnum.FLAG_SHOW_REPORT.value: True,
            # 检测版本更新
            GlobalConfigEnum.FLAG_CHECK_UPDATE.value: True,
            # 使用配置文件链接导出数据
            GlobalConfigEnum.FLAG_USE_CONFIG_URL.value: True,
            # 使用原神日志文件导出数据
            GlobalConfigEnum.FLAG_USE_LOG_URL.value: True,
            # 导出到txt
            GlobalConfigEnum.FLAG_WRITE_TXT.value:True,
            # 导出到xlsx
            GlobalConfigEnum.FLAG_WRITE_XLSX.value: True,
        }
        self.read()

        self.save()
    
    @catchException("配置文件加载失败", "debug")
    def read(self):
        super().read()

    @catchException("配置文件写入失败")
    def save(self):
        super().save()
        logger.debug("重新写入配置文件")

class UserConfigEnum(Enum):
    """
    用户配置项枚举
    """
    URL = "URL"
    UID = "UID"


class UserConfig(BaseConfig):
    
    def __init__(self, uid) -> None:
        super().__init__()
        self.uid = str(uid)
        self.setting = {
            UserConfigEnum.UID.value:uid,
            UserConfigEnum.URL.value:"",
        }
        user_dir = os.path.join(self.path, uid)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        self.path = os.path.join(user_dir, "config.json")
        
        self.read()
        self.save()
    
    @catchException("用户配置文件加载失败", "debug")
    def read(self):
        super().read()

    @catchException("用户配置文件写入失败")
    def save(self):
        super().save()
        logger.debug("重新写入用户配置文件")

