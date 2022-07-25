import json
import os
import sys

import requests
from tqdm import tqdm

from genshin import __version__ as version
from genshin.common import CommonEnum
from genshin.utils.logger import logger


def get_latest_version_info():
    """
    获取最新的 Release 信息

    例如:
    ("1.0.0", [{"name":"win10", "url":"https://xxx"}])

    :Return:
    tag_name: 版本名
    download_info: 版本包含的可下载文件url
    """

    r = requests.get("https://api.github.com/repos/dantkv/Genshin-Impact-Tools/releases/latest")
    data = json.loads(r.content.decode("utf-8"))
    tag_name = data["tag_name"]
    if tag_name[0] == "v":
        tag_name = tag_name[1:]

    download_info = []
    for asset in data["assets"]:
        info = {}
        info["name"] = asset["name"]
        info["url"] = asset["browser_download_url"]
        download_info.append(info)
    return tag_name, download_info


def get_sys_name():
    name = "win10"
    if sys.getwindowsversion().major < 10:
        name = "win7"
    return name


def get_download_url(info):
    """
    根据系统版本获得对应文件链接
    """

    sys_name = get_sys_name()

    for i in info:
        if i["name"].find(sys_name) >= 0:
            return i["name"], i["url"]
    return None, None


def check_update():
    """
    检测是否需要更新软件
    """
    logger.info("检测软件更新……")
    tag_name, download_info = get_latest_version_info()
    if version == tag_name:
        return None

    else:
        return download_info


def download(path: str, url: str):
    with open(path, "wb") as file:
        with requests.get(url, stream=True) as r:
            total_length = int(r.headers.get("content-length", 0))
            with tqdm(total=total_length, unit="B", unit_scale=True) as pbar:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        pbar.update(1024)


def upgrade():
    """
    升级软件
    """
    download_info = check_update()
    if not download_info:
        logger.info("软件已是最新")
        return

    logger.warning("正在更新软件，请误关闭窗口")
    name, url = get_download_url(download_info)
    if not os.path.exists(CommonEnum.TEMP_PATH.value):
        os.mkdir(CommonEnum.TEMP_PATH.value)
    # 下载文件
    file_path = os.path.join(CommonEnum.TEMP_PATH.value, name)
    download(file_path, url)

    logger.info("文件下载完成，请解压替换文件")
    logger.info("文件位于{}", file_path)
    return True
