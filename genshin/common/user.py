import os

from genshin.common.const import CommonEnum


class UserDataEnum:
    """
    用户数据存储路径枚举
    """

    def __init__(self, uid=None) -> None:
        self.update(uid)

    def update(self, uid):
        """
        更新用户设置
        """
        if not uid:
            self.uid = UserDataEnum.get_uid()
        else:
            self.uid = uid
        # 用户数据根目录
        self.user_data_path = os.path.join(CommonEnum.DATA_PATH.value, str(self.uid))
        # 抽卡记录文件路径
        self.gacha_data_file_path = os.path.join(self.user_data_path, "gacha_data.json")
        # 统计结果路径
        self.result_file_path = os.path.join(self.user_data_path, "result.json")
        # 配置文件路径
        self.result_file_path = os.path.join(self.user_data_path, "config.json")

    @staticmethod
    def get_uid():
        """
        从游戏文件获取UID
        """

        uid_info_file = os.path.join(
            CommonEnum.USERPROFILE.value,
            "AppData",
            "LocalLow",
            "miHoYo",
            "原神",
            "UidInfo.txt",
        )
        with open(uid_info_file, "r", encoding="utf-8", errors="ignore") as f:
            uid = f.readline().rstrip()
        return uid


USER_DATA_ENUM = UserDataEnum()
