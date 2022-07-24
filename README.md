# 原神小工具

## 主要功能：
- 抽卡数据导出（由于官方限制，只能导出最近6个月抽卡记录）
- 抽卡数据统计显示
- 支持多账户使用

## 抽卡结果示例

<table border="1">
    <tr>
        <td><img src="https://raw.githubusercontent.com/wiki/dantkv/Genshin-Impact-Tools/resource/gacha_report.png" alt="抽卡报告示例" style="zoom:80%;"></td>
        <td><img src="https://raw.githubusercontent.com/wiki/dantkv/Genshin-Impact-Tools/resource/gacha_log.png" alt="抽卡日志示例" style="zoom:80%;"></td>
    </tr>
</table>

## 如何使用

### 下载

在软件 [下载页面][3] 找到对应系统的软件版本下载ZIP压缩包解压
- Win10 及以上版本无后缀， 对应文件名为 **`Genshin_Impact_Tools.zip`**
- Win7 版本后缀为_win7， 对应文件名为 **`Genshin_Impact_Tools_win7.zip`**

### 使用步骤

1. 运行游戏，打开抽卡记录页面
2. 运行本软件，等待记录导出完成
3. 报告生成后，在程序所在目录的 `data` 文件夹下可找到抽卡报告文件

- **如何切换其他用户**
  1. 游戏内切换账户
  2. 进入游戏并打开抽卡记录界面
  3. 关闭本软件后重新打开
  4. 等待数据导出


### 注意事项
程序运行会在程序所在目录生成两个文件夹 `log` 和 `data` 文件夹

`data` 文件夹如果有历史导出记录，会自动和最新记录合并，若希望保留历史记录请**不要删除**该文件夹

```sh
.
├── Genshin_Impact_Tools.exe
├── data
│   ├── 204600873 # 用户存储目录
│   │   ├── config.json # 用户配置文件
│   │   ├── gacha_data.json # 原始抽卡数据
│   │   ├── 抽卡报告.txt
│   │   └── 抽卡数据总览.xlsx
│   └── config.json # 软件设置文件
└── log # 日志目录
    └── log_2022-06.log
```

更多信息见 [**Wiki 帮助指南**][2]

### Commit 规范

https://www.conventionalcommits.org/zh-hans/v1.0.0

---

本项目基于项目 **[genshin-gacha-export][1]** 修改而来


[1]:https://github.com/sunfkny/genshin-gacha-export
[2]:https://github.com/dantkv/Genshin-Impact-Tools/wiki
[3]:https://github.com/dantkv/Genshin-Impact-Tools/releases/latest