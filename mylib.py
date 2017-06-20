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

def get_win_option_handle(win_title):
    """
    获取配置Option窗口的句柄
    :return: 返回句柄；不成功则返回0
    """

    # 逐级查找配置芯片Button的handle
    hwnd_main = win32gui.FindWindow(None, 'EZPro100')
    hwnd_group_tool = win32gui.FindWindowEx(
        hwnd_main, 0, None, TOOL_GROUP_TEXT)
    hwnd_cmd_config = win32gui.FindWindowEx(
        hwnd_group_tool, 0, None, CONFIG_BUTTON_TEXT)

    # 点击配置芯片Button，打开Option窗口
    if hwnd_cmd_config != 0:
        win32api.PostMessage(hwnd_cmd_config, win32con.BM_CLICK, 0, 0)
        time.sleep(1)  # 需等待窗口打开，方能进行FindWindow，0.3s比较可靠
        return win32gui.FindWindow(None, win_title)
    else:
        return 0