import json
import os
import sys

import requests
from tqdm import tqdm

from genshin.common import CommonEnum
from genshin.utils.functional import press_any_key_to_exit
from genshin.utils.logger import logger


def get_latest_version_info():
    """
    获取最后的Release信息
    """

    r = requests.get("https://api.github.com/repos/dantkv/Genshin-Impact-Tools/releases/latest")
    data = json.loads(r.content.decode("utf-8"))
    tag_name = data["tag_name"]
    download_info = list()
    for asset in data["assets"]:
        info = dict()
        info["name"] = asset["name"]
        info["url"] = asset["browser_download_url"]
        download_info.append(info)
    return tag_name, download_info


def check_version(tag_name):
    """
    检查软件版本是否需要更新

    :return
    False 不需要更新
    """
    with open(os.path.join(CommonEnum.RESOURCE_FILE_PATH.value, "version.info"), "r", encoding="utf8") as f:
        version_info = json.load(f)
        version = version_info["version"]
    if version != tag_name:
        return True
    return False


def update_version():
    """
    更新软件版本号
    """

    def get_next_version(version):
        """
        版本号+1
        """

        nums = version.split(".")
        # 去除v开头
        nums[0] = nums[0][1:]
        i = len(nums) - 1
        remainder = 1
        while i >= 0:
            nums[i] = int(nums[i])
            divisor = int((nums[i] + remainder) % 10)
            remainder = int((nums[i] + remainder) / 10)
            nums[i] = str(divisor)
            if remainder == 0:
                break
            i = i - 1
        nums[0] = "v" + nums[0]
        return ".".join(nums)

    tag_name, download_info = get_latest_version_info()
    version_info = dict()
    version_info["version"] = get_next_version(tag_name)
    with open(os.path.join(CommonEnum.RESOURCE_FILE_PATH.value, "version.info"), "w", encoding="utf8") as f:
        json.dump(version_info, f, ensure_ascii=False, sort_keys=False, indent=4)

    return download_info


def get_url_from_system(info):
    """
    根据系统版本获得对应文件链接
    """

    end_str = "_Tools.zip"
    if sys.getwindowsversion().major < 10:
        end_str = "_win7.zip"

    for i in info:
        if i["name"].endswith(end_str):
            return i["name"], i["url"]


def upgrade():
    """
    升级软件
    """
    logger.info("检测软件更新……")
    tag_name, download_info = get_latest_version_info()

    if not check_version(tag_name):
        logger.info("软件已是最新")
        return
    logger.warning("正在更新软件，请误关闭窗口")

    name, url = get_url_from_system(download_info)

    if not os.path.exists(CommonEnum.TEMP_PATH.value):
        os.mkdir(CommonEnum.TEMP_PATH.value)

    # 下载文件
    download_file_path = os.path.join(CommonEnum.TEMP_PATH.value, name)

    with open(download_file_path, "wb") as file:
        with requests.get(url, stream=True) as r:
            total_length = int(r.headers.get("content-length", 0))
            with tqdm(total=total_length, unit="B", unit_scale=True) as pbar:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        pbar.update(1024)

    logger.info("文件下载完成，请解压替换文件")
    logger.info("文件位于{}", download_file_path)

    press_any_key_to_exit()
