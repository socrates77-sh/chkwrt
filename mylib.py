"""定义通用的函数、常数"""

import os
import win32api
import win32gui
import win32con
import time

LOG_FILE_NAME = 'result.log'  # LOG文件名
EZPRO_TITLE = 'EZPro100'  # EZPro100程序主窗口标题
TOOL_GROUP_TEXT = '快捷工具栏'  # 快捷工具Group标题
CONFIG_BUTTON_TEXT = '配置芯片'  # 配置芯片Button标题
OPTION_CANCEL_BUTTON_TEXT = '取消'  # 配置窗口<取消>Button标题
OPTION_OK_BUTTON_TEXT = '确定'  # 配置窗口<确定>Button标题
WAIT_SECOND = 1  # 按键后等待的时间


# 创建LOG文件
try:
    f_log = open(LOG_FILE_NAME, 'w')
except:
    print('Cannot open %s!' % LOG_FILE_NAME)


def log_print(s, end='\n'):
    print(s, end=end)
    print(s, end=end, file=f_log)


def get_process_count(process_name):
    """
    利用tasklist查询活动的task个数
    :param process_name: task栏中的名称，包括后缀.exe
    :return: 查询到task的个数
    """
    p = os.popen('tasklist /FI "IMAGENAME eq %s"' % process_name)
    return p.read().count(process_name)
