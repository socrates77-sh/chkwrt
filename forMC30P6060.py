#!/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zwr'

from mylib import *
import win32api
import win32gui
import win32con
import time
import struct

Product_Type_Name = 'MC30P6060'  # 品名
Option_Win_Title = '配置 MC30P6060'  # 配置Option的窗口标题

# 全局变量，遍历option窗口空间的序号
index_of_control = 0


def get_win_option_handle():
    """
    获取配置Option窗口的句柄
    :return: 返回句柄；不成功则返回0
    """

    # 逐级查找配置芯片Button的handle
    hwnd_main = win32gui.FindWindow(None, 'EZPro100')
    hwnd_group_tool = win32gui.FindWindowEx(hwnd_main, 0, None, TOOL_GROUP_TEXT)
    hwnd_cmd_config = win32gui.FindWindowEx(hwnd_group_tool, 0, None, CONFIG_BUTTON_TEXT)

    # 点击配置芯片Button，打开Option窗口
    if hwnd_cmd_config != 0:
        win32api.PostMessage(hwnd_cmd_config, win32con.BM_CLICK, 0, 0)
        time.sleep(0.3)  # 需等待窗口打开，方能进行FindWindow，0.3s比较可靠
        return win32gui.FindWindow(None, Option_Win_Title)
    else:
        return 0


def do_TRadioButton_value(hwnd):
    result = win32api.SendMessage(hwnd, win32con.BM_GETCHECK, 0, 0)
    print('  (Value)%d' % result, file=f_log)


def do_TComboBox_value(hwnd):
    selected_index = win32api.SendMessage(hwnd, win32con.CB_GETCURSEL, 0, 0)
    if selected_index == -1:
        selected_text = '<no select>'
    else:
        # buf = win32gui.PyMakeBuffer(256)
        # n = win32api.SendMessage(hwnd, win32con.CB_GETLBTEXT, selected_index, buf)
        pass

    print('  (Value)%d %s' % (selected_index, selected_index), file=f_log)


def do_control(hwnd, lparam):
    """
    EnumChildWindows需要的EnumWindowsCallback函数
    :param hwnd: EnumChildWindows获取的hwnd
    :param lparam: EnumChildWindows获取的lparam
    :return: None
    """

    # 获取空间的text和class_name
    global index_of_control
    control_text = win32gui.GetWindowText(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    print('[%02d](class)%-20s(text)%s' % (index_of_control, control_text, class_name), end='', file=f_log)

    if class_name == 'TRadioButton':
        do_TRadioButton_value(hwnd)
    elif class_name == 'TComboBox':
        do_TComboBox_value(hwnd)
    else:
        print('', file=f_log)

    index_of_control += 1


def extract_win_option():
    """
    提取Option窗口的信息
    :return:
    """
    hwnd = get_win_option_handle()

    # 遍历Option窗口的所有控件
    global index_of_control
    index_of_control = 0
    win32gui.EnumChildWindows(hwnd, do_control, 0)


def check_all():
    print('=======================================================================================', file=f_log)
    print('\t%s' % Product_Type_Name, file=f_log)
    print('=======================================================================================', file=f_log)
    extract_win_option()