"""定义通用的函数、常数"""

# !/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'zwr'

LOG_FILE_NAME = 'result.log'  # LOG文件名
EZPRO_TITLE = 'EZPro100'  # EZPro100程序主窗口标题
TOOL_GROUP_TEXT = '快捷工具栏'  # 快捷工具Group标题
CONFIG_BUTTON_TEXT = '配置芯片'  # 配置芯片Button标题

import os

# 创建LOG文件
try:
    f_log = open(LOG_FILE_NAME, 'w')
except:
    print('Cannot open %s!' % LOG_FILE_NAME)


def get_process_count(process_name):
    """
    利用tasklist查询活动的task个数
    :param process_name: task栏中的名称，包括后缀.exe
    :return: 查询到task的个数
    """
    p = os.popen('tasklist /FI "IMAGENAME eq %s"' % process_name)
    return p.read().count(process_name)

