import os
import traceback

from genshin.common.const import CommonEnum
from genshin.common.user import USER_DATA_ENUM
from genshin.config import GlobalConfig, GlobalConfigEnum, UserConfig
from genshin.module import update
from genshin.module.gacha_export import GachaExportTool
from genshin.utils.functional import press_any_key_to_exit
from genshin.utils.logger import logger


def run():
    global_config = GlobalConfig()
    logger.debug(CommonEnum.ROOT_PATH.value)
    logger.debug(CommonEnum.DATA_PATH.value)
    if not os.path.exists(CommonEnum.DATA_PATH.value):
        os.mkdir(CommonEnum.DATA_PATH.value)

    logger.debug("config" + str(global_config.setting))
    if global_config.get_key(GlobalConfigEnum.FLAG_CHECK_UPDATE.value):
        try:
            if update.upgrade():
                press_any_key_to_exit()
        except Exception:
            logger.warning("检查更新失败")
            logger.debug(traceback.format_exc())

    # 设置用户
    user_config = UserConfig(USER_DATA_ENUM.uid)
    logger.info("当前用户为：{}", USER_DATA_ENUM.uid)
    gacha_export_tool = GachaExportTool(user_config)

    if global_config.get_key(GlobalConfigEnum.FLAG_WRITE_TXT.value):
        gacha_export_tool.generator_txt()
    if global_config.get_key(GlobalConfigEnum.FLAG_WRITE_XLSX.value):
        gacha_export_tool.generator_xlsx()

    # 导出数据
    if global_config.get_key(GlobalConfigEnum.FLAG_USE_CONFIG_URL.value):
        status = gacha_export_tool.get_gacha_log_by_config()
    if not status and global_config.get_key(GlobalConfigEnum.FLAG_USE_LOG_URL.value):
        status = gacha_export_tool.get_gacha_log_by_game_log()

    press_any_key_to_exit()


if __name__ == "__main__":
    run()
