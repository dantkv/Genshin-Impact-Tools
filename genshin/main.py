import os
import traceback

from genshin.common import USER_DATA_ENUM, CommonEnum
from genshin.config import GlobalConfig, GlobalConfigEnum, UserConfig
from genshin.module import update
from genshin.module.gacha_export import GachaExportTool
from genshin.utils.functional import pressAnyKeyToExit
from genshin.utils.logger import logger


class Main:
    def __init__(self) -> None:
        self._manu = []
        self._global_config = GlobalConfig()
        logger.debug(CommonEnum.ROOT_PATH.value)
        logger.debug(CommonEnum.DATA_PATH.value)
        if not os.path.exists(CommonEnum.DATA_PATH.value):
            os.mkdir(CommonEnum.DATA_PATH.value)

        logger.debug("config" + str(self._global_config.setting))

    def run(self):
        # 检测软件更新
        if self._global_config.get_key(GlobalConfigEnum.FLAG_CHECK_UPDATE.value):
            try:
                update.upgrade()
            except Exception:
                logger.warning("检查更新失败")
                logger.debug(traceback.format_exc())

        # 设置用户
        user_config = UserConfig(USER_DATA_ENUM.uid)
        logger.info("当前用户为：{}", USER_DATA_ENUM.uid)
        gacha_export_tool = GachaExportTool(user_config)

        if self._global_config.get_key(GlobalConfigEnum.FLAG_WRITE_TXT.value):
            gacha_export_tool.generatorTXT()
        if self._global_config.get_key(GlobalConfigEnum.FLAG_WRITE_XLSX.value):
            gacha_export_tool.generatorXLSX()

        # 导出数据
        if self._global_config.get_key(GlobalConfigEnum.FLAG_USE_CONFIG_URL.value):
            status = gacha_export_tool.getGachaLogByConfig()
        if not status and self._global_config.get_key(GlobalConfigEnum.FLAG_USE_LOG_URL.value):
            status = gacha_export_tool.getGachaLogByGameLog()

        pressAnyKeyToExit()


if __name__ == "__main__":
    main = Main()
    main.run()
