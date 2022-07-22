import json
import os
import requests
import time
import traceback
from enum import Enum
from urllib import parse
from random import random
from utils import catchException
from utils import logger
from common import USER_DATA_ENUM
from common import CommonEnum
from config import UserConfig
from config import UserConfigEnum


class GachaTypeEnum(Enum):
    """
    抽卡类型枚举
    """
    # 抽卡类型ID
    GACHA_QUERY_TYPE_IDS = ["100", "200", "301", "302"]

    # 抽卡类型名
    GACHA_QUERY_TYPE_NAMES = ["新手祈愿", "常驻祈愿", "角色活动祈愿", "武器活动祈愿"]

    GACHA_QUERY_TYPE_DICT = dict(zip(GACHA_QUERY_TYPE_IDS, GACHA_QUERY_TYPE_NAMES))
    
    GACHA_TYPE_DICT = {
        "100": "新手祈愿",
        "200": "常驻祈愿",
        "301": "角色活动祈愿",
        "302": "武器活动祈愿",
        "400": "角色活动祈愿-2"
    }


class GachaData:
    """
    抽卡数据类
    """
    def __init__(self, url:str, uid:str) -> None:
        self.uid = uid
        self.url = url
        # 抽卡数据
        self.data = dict()

    @catchException("保存抽卡记录失败")
    def saveData(self):
        """
        保存抽卡数据
        """
        with open(USER_DATA_ENUM.GACHA_DATA_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, sort_keys=False, indent=4)
        return True
    
    def _mergeData(self, merge_data:dict):
        """
        合并历史查询记录
        """
        if not self.data:
            return merge_data
        for gacha_type in GachaTypeEnum.GACHA_QUERY_TYPE_DICT.value:
            history_gacha_log = merge_data["gacha_log"][gacha_type]
            new_gacha_log = self.data["gacha_log"][gacha_type]
            if len(history_gacha_log):
                history_latest_data = history_gacha_log[-1]
                # 根据抽卡id比较大小，找出新的抽卡记录并保存在 temp_gacha_data
                temp_gacha_data = [log for log in new_gacha_log if log["id"] > history_latest_data["id"]]
            else:
                temp_gacha_data = new_gacha_log
            
            history_gacha_log.extend(temp_gacha_data)
            logger.info(f"抽卡历史记录合并 =====+> { GachaTypeEnum.GACHA_QUERY_TYPE_DICT.value[gacha_type] } \t增加了 { len(temp_gacha_data) } \t条记录")
        
        return merge_data

    def mergeHistoryData(self):
        """
        合并历史记录
        """
        @catchException("历史抽卡记录文件读取失败")
        def loadHistory():
            if not os.path.exists(USER_DATA_ENUM.GACHA_DATA_FILE_PATH):
                logger.debug("历史抽卡记录文件不存在")
                return None
            with open(USER_DATA_ENUM.GACHA_DATA_FILE_PATH, "r", encoding="UTF-8") as f:
                history_data = json.load(f)
            return history_data
        
        history_data = loadHistory()
        if history_data:
            self.data = self._mergeData(history_data)

    def _getGachaLogsByTypeId(self, gacha_type_id):
        """
        根据抽卡类型查询抽卡记录
        """
        size = "20"
        # api限制一页最大20
        gacha_list = []
        end_id = "0"
        for page in range(1, 9999):
            logger.info(f"正在获取 {GachaTypeEnum.GACHA_QUERY_TYPE_DICT.value[gacha_type_id]} 第 {page} 页")
            api = self._updateQueryURL(gacha_type_id, size, page, end_id)
            r = requests.get(api).content.decode("utf-8")
            j = json.loads(r)
            gacha = j["data"]["list"]
            if not len(gacha):
                break
            for i in gacha:
                gacha_list.append(i)
            end_id = j["data"]["list"][-1]["id"]
            time.sleep(0.5+random())
        return gacha_list

    def _updateQueryURL(self, gacha_type, size, page, end_id=""):
        """
        设置分页查询参数
        """
        parsed = parse.urlparse(self.url)
        querys = parse.parse_qsl(str(parsed.query))
        param_dict = dict(querys)

        param_dict["size"] = size
        param_dict["gacha_type"] = gacha_type
        param_dict["page"] = page
        param_dict["lang"] = "zh-cn"
        param_dict["end_id"] = end_id

        param = parse.urlencode(param_dict)

        path = str(self.url).split("?")[0]
        api = path + "?" + param
        return api
    
    def getGachaLog(self):
        """
        获取最近6个月抽卡记录
        """
        logger.info("开始获取抽卡记录")
        
        self.data["uid"] = self.uid
        self.data["gacha_type"] = GachaTypeEnum.GACHA_QUERY_TYPE_DICT.value
        self.data["gacha_log"] = {}

        for gacha_type_id in GachaTypeEnum.GACHA_QUERY_TYPE_IDS.value:
            # 查询时间顺序由近到远
            gachaLog = self._getGachaLogsByTypeId(gacha_type_id)
            # 翻转后正序排列
            gachaLog.reverse()
            self.data["gacha_log"][gacha_type_id] = gachaLog

        return self.data
    
    

class BaseGenerator:
    
    def __init__(self, data = None) -> None:
        self._data=data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
    
    def generator(self):
        pass
    


class GeneratorXLSX(BaseGenerator):
    def __init__(self, data=None) -> None:
        super().__init__(data)

    def generator(self):
        from xlsxwriter import Workbook

        workbook_path = os.path.join(USER_DATA_ENUM.USER_DATA_PATH, "抽卡数据总览.xlsx")
        logger.debug("创建工作簿: " + workbook_path)
        workbook = Workbook(workbook_path)
        
        # 初始化标题栏和正文默认
        content_css = workbook.add_format({"align": "left", "font_name": "微软雅黑", "border_color": "#c4c2bf", "bg_color": "#ebebeb", "border": 1})
        title_css = workbook.add_format({"align": "left", "font_name": "微软雅黑", "color": "#757575", "bg_color": "#dbd7d3", "border_color": "#c4c2bf", "border": 1, "bold": True})
        
        star_5 = workbook.add_format({"color": "#bd6932", "bold": True})
        star_4 = workbook.add_format({"color": "#a256e1", "bold": True})
        star_3 = workbook.add_format({"color": "#8e8e8e"})

        for gacha_type_id in GachaTypeEnum.GACHA_QUERY_TYPE_IDS.value:
            gacha_type_List = self._data["gacha_log"][gacha_type_id][:]
            gacha_type_name = GachaTypeEnum.GACHA_TYPE_DICT.value[gacha_type_id]

            logger.debug("开始写入 {}, 共 {} 条数据", gacha_type_name, len(gacha_type_List))
            worksheet = workbook.add_worksheet(gacha_type_name)
            excel_header = ["总次数", "时间", "名称", "类别", "星级", "祈愿类型", "保底内"]

            # 设置列宽
            worksheet.set_column("B:B", 22)
            worksheet.set_column("C:C", 14)
            worksheet.set_column("F:F", 16)
            
            worksheet.write_row(0, 0, excel_header, title_css)
            
            worksheet.freeze_panes(1, 0)

            total_counter = 0
            pity_counter = 0
            for gacha in gacha_type_List:
                time_str = gacha["time"]
                name = gacha["name"]
                item_type = gacha["item_type"]
                rank_type = int(gacha["rank_type"])
                gacha_type = gacha["gacha_type"]
                gacha_type_name = GachaTypeEnum.GACHA_TYPE_DICT.value.get(gacha_type, "")
                total_counter = total_counter + 1
                pity_counter = pity_counter + 1
                excel_data = [ total_counter, time_str, name, item_type, rank_type, gacha_type_name, pity_counter]
                worksheet.write_row(total_counter, 0, excel_data, content_css)
                if rank_type == 5:
                    pity_counter = 0

            first_row = 1  # 不包含表头第一行 (zero indexed)
            first_col = 0  # 第一列
            last_row = len(gacha_type_List)  # 最后一行
            last_col = len(excel_header) - 1  # 最后一列，zero indexed 所以要减 1
            worksheet.conditional_format(first_row, first_col, last_row, last_col, {"type": "formula", "criteria": "=$E2=5", "format": star_5})
            worksheet.conditional_format(first_row, first_col, last_row, last_col, {"type": "formula", "criteria": "=$E2=4", "format": star_4})
            worksheet.conditional_format(first_row, first_col, last_row, last_col, {"type": "formula", "criteria": "=$E2=3", "format": star_3})

        workbook.close()
        logger.debug("工作簿写入完成")
        return True

class GeneratorTXT(BaseGenerator):
    def __init__(self, data=None) -> None:
        super().__init__(data)
        self.result = {}
    
    def gachaLogCounter(self):
        """
        统计数据并保存
        """
        # TODO 添加3星各类武器统计数量
        gacha_log = self._data["gacha_log"]
        self.result["uid"] = self._data["uid"]
        for gacha_type_id in gacha_log:
            # 取得每类抽卡数据字典
            gacha_list = gacha_log[gacha_type_id]
            
            self.result[gacha_type_id] = {}
            result_type = self.result[gacha_type_id]
            result_type["name"] = self._data["gacha_type"][gacha_type_id]
            result_type["total_count"] = len(gacha_list)
            if not len(gacha_list):
                continue
            logger.debug("卡池: {} \t抽卡总数: {} \t", result_type["name"], result_type["total_count"] )

            def reduce_data(data:None, count:None):
                """
                处理查询记录，减少不必要数据
                """
                result = {}
                result["time"] = data["time"] 
                result["name"] = data["name"]
                result["item_type"] = data["item_type"]
                result["rank_type"] = data["rank_type"]
                result["before_count"] = count
                return result
            
            # 统计4, 5星数据
            result_type["5"] = []
            result_type["4"] = []
            result_type["start_time"] = gacha_list[0]["time"]
            result_type["end_time"] = gacha_list[-1]["time"]
            before_count_level_5 = 0
            before_count_level_4 = 0
            for log in gacha_list:
                if log["rank_type"] == "4":
                    result_type["4"].append(reduce_data(log, before_count_level_4))
                    before_count_level_4 = 0
                elif log["rank_type"] == "5":
                    result_type["5"].append(reduce_data(log, before_count_level_5))
                    before_count_level_5 = 0

                if log["rank_type"] != "4":
                    before_count_level_4 = before_count_level_4+1
                if log["rank_type"] != "5":
                    before_count_level_5 = before_count_level_5+1
            # 记录最后的抽卡次数
            result_type["last_gacha_count"] = before_count_level_5
    
        return self.result
    
    def generator(self):
        """
        生成抽卡报告
        """
        self.gachaLogCounter()

        if not self.result:
            logger.error("抽卡统计结果为空")
            return False
        
        def report_template(temp_info:dict):
            level_5_info = []
            
            for log in data["5"]:
                info = f"{ log['name'] }@{ log['before_count']+1 }抽"
                level_5_info.append(info)
            
            return f"卡池: { temp_info['name'] }\n抽卡时间: { temp_info['start_time'][:-3] } 至 { temp_info['end_time'][:-3] }\n"\
                f"抽卡总数: { temp_info['total_count'] }\n"\
                f"5星数量: { len(temp_info['5']) }\n5星详情: { ','.join(level_5_info) }\n"\
                f"距上次出5星已累计抽卡次数: { temp_info['last_gacha_count'] }\n"
        
        logger.debug("开始生成TXT报告……")
        reports = []
        for gacha_type_id in GachaTypeEnum.GACHA_QUERY_TYPE_IDS.value:
            data = self.result[gacha_type_id]
            if not data["total_count"]:
                reports.append(f"{data['name']}无抽卡记录\n")
                continue
            reports.append(report_template(data))
        
        @catchException("抽卡报告保存失败")
        def saveReport():
            """
            保存抽卡报告
            """
            with open(os.path.join(USER_DATA_ENUM.USER_DATA_PATH, "抽卡报告.txt"), "w", encoding="utf-8") as f:
                f.write("\n".join(reports))
            return True
        
        return saveReport()


class GachaReport:
    """
    抽卡报告类
    """
    def __init__(self, data:dict = None, generator_list:list = []) -> None:
        """
        data: 原始抽卡记录
        """
        self._data = data
        self.generator_list = generator_list
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value
    
    def addGenerator(self, generaotor):
        self.generator_list.append(generaotor)

    def removeGenerator(self, generaotor):
        self.generator_list.remove(generaotor)

    def runGenerator(self):
        logger.info("开始生成报告……")
        result = True
        for generator in self.generator_list:
            generator.data = self.data
            result = result & generator.generator()
        logger.info("抽卡统计已完成")
        return result


class GachaExportTool:
    """
    抽卡导出工具类
    """
    def __init__(self, user_config:UserConfig) -> None:
        self.user_config = user_config
        self.uid = user_config.uid
        self.report = GachaReport()

    def _export_data(self, url:str):
        gacha_data = GachaData(url, self.uid)
        gacha_data.getGachaLog()
        gacha_data.mergeHistoryData()
        gacha_data.saveData()

        self.report.data = gacha_data.data
        return self.report.runGenerator()

    def _checkURL(self, url:str):
        """
        测试查询链接有效性
        """
        try:
            r = requests.get(url).content.decode("utf-8")
            j = json.loads(r)
        except Exception:
            logger.error("API请求解析出错")
            logger.debug(traceback.format_exc())
            return False
        
        logger.debug(j)
        if not j["data"]:
            if j["message"] == "authkey timeout":
                logger.warning("链接过期")
            elif j["message"] == "authkey error":
                logger.warning("链接错误")
            else:
                logger.warning("数据为空，错误代码：" + j["message"])
            return False
        
        return True

    def _getQueryURL(self, url):
        logger.debug("log url =====> {}", url)
        spliturl = str(url).split("?")
        if "webstatic-sea" in spliturl[0] or "hk4e-api-os" in spliturl[0]:
            spliturl[0] = "https://hk4e-api-os.mihoyo.com/event/gacha_info/api/getGachaLog"
        else:
            spliturl[0] = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog"
        url = "?".join(spliturl)
        return url
    
    def getGachaLogByConfig(self):
        """
        使用配置文件查询抽卡日志
        """
        logger.info("检查配置文件中的链接")
        url = self.user_config.getKey(UserConfigEnum.URL.value)
        if not url or "?" not in url:
            logger.warning("配置文件中链接为空")
            return False
        
        url = self._getQueryURL(url)
        if not self._checkURL(url):
            return False
        logger.info("配置文件中的链接可用，将使用该链接导出数据")
        logger.debug("config file url =====> {}", url)
        return self._export_data(url)
    
    def getGachaLogByGameLog(self):
        """
        使用游戏日志文件链接查询抽卡日志
        """
        logger.info("尝试使用日志文件中的链接导出数据")
        game_log_path = ""
        game_log_path_cn = os.path.join(CommonEnum.USERPROFILE.value, "AppData", "LocalLow", "miHoYo", "原神", "output_log.txt")
        game_log_path_global = os.path.join(CommonEnum.USERPROFILE.value, "AppData", "LocalLow", "miHoYo", "Genshin Impact", "output_log.txt")

        if os.path.isfile(game_log_path_cn):
            logger.debug("检测到国服日志文件")
            logger.debug("game_log_path_cn: " + game_log_path_cn)
            game_log_path = game_log_path_cn

        if os.path.isfile(game_log_path_global):
            logger.debug("检测到海外服日志文件")
            logger.debug("game_log_path_global: " + game_log_path_global)
            game_log_path = game_log_path_global

        if os.path.isfile(game_log_path_cn) and os.path.isfile(game_log_path_global):
            flag = True
            while flag:
                logger.info("检测到两个日志文件, 输入1选择国服, 输入2选择海外服, 输入0退出")
                c = input()
                if c == "1":
                    game_log_path = game_log_path_cn
                    flag = False
                elif c == "2":
                    game_log_path = game_log_path_global
                    flag = False
                elif c == "0":
                    exit()
                else :
                    logger.info("输入有误, 重新输入")

        def getURLFromLog(game_log_path=None):
            """
            从日志文件提取抽卡链接
            """
            @catchException()
            def readLogFile(path):
                if not os.path.isfile(path):
                    logger.warning("未检测到日志文件")
                    return ""
                with open(path, "r", encoding="mbcs", errors="ignore") as f:
                    log = f.readlines()
                return log
            url = None
            log = readLogFile(game_log_path)
            line_number = 0
            for line in log:
                line_number = line_number+1
                if line.startswith("OnGetWebViewPageFinish:") and line.endswith("#/log\n"):
                    url = line.replace("OnGetWebViewPageFinish:", "").replace("\n", "")
            return url

        url = getURLFromLog(game_log_path)
        if not url:
            logger.error("日志文件中没有链接，请打开游戏抽卡历史记录界面后重试")
            return False
    
        url = self._getQueryURL(url)
        logger.debug("检查日志文件中的链接")
        if not self._checkURL(url):
            logger.info("请打开游戏抽卡界面后重试")
            return False
        self.user_config.setKey(UserConfigEnum.URL.value, url)
        return self._export_data(url)

    def generatorTXT(self):
        self.report.addGenerator(GeneratorTXT())
    
    def generatorXLSX(self):
        self.report.addGenerator(GeneratorXLSX())
