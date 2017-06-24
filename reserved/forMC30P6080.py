from mylib import *
import win32api
import win32gui
import win32con
import time
# import struct

Product_Type_Name = 'MC30P6080'  # 品名
Option_Win_Title = '配置 MC30P6080'  # 配置Option的窗口标题

# 全局变量，遍历option窗口空间的序号
index_of_control = 0

all_hwnd_TComboBox = []
all_hwnd_TRadioButton = []


def do_TRadioButton_value(hwnd):
    result = win32api.SendMessage(hwnd, win32con.BM_GETCHECK, 0, 0)
    log_print('  (Value)%d' % result)


def do_TComboBox_value(hwnd):
    selected_index = win32api.SendMessage(hwnd, win32con.CB_GETCURSEL, 0, 0)
    if selected_index == -1:
        info_text = '<no select>'
    else:
        buf_len = win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH) + 1
        buf_len *= 2  # 汉字需*2
        buf = win32gui.PyMakeBuffer(buf_len)
        win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_len, buf)
        info_text = buf.tobytes().decode('utf_16_le', 'ignore')
        pass

    log_print('  (Value)%d %s' % (selected_index, info_text))


def gather_all_TComBox(hwnd):
    '''
    将抓取到可见的TComBox的hwnd存到list中
    '''
    if(win32gui.IsWindowVisible(hwnd)):
        all_hwnd_TComboBox.append(hwnd)


def gather_all_TRadioButton(hwnd):
    '''
    将抓取到可见的TRadioButton的hwnd存到list中
    '''
    if(win32gui.IsWindowVisible(hwnd)):
        all_hwnd_TRadioButton.append(hwnd)


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
    # log_print('[%02d](class)%-20s(text)%s' %
    #           (index_of_control, control_text, class_name), end='')

    if class_name == 'TRadioButton':
        gather_all_TRadioButton(hwnd)
    elif class_name == 'TComboBox':
        gather_all_TComBox(hwnd)
    else:
        # log_print('')
        pass

    index_of_control += 1


def extract_win_option():
    """
    提取Option窗口的信息
    :return:
    """
    hwnd = get_win_option_handle(Option_Win_Title)

    if(hwnd == 0):
        print('Not find option window')
        exit(2)

    # 遍历Option窗口的所有控件
    global index_of_control
    index_of_control = 0
    win32gui.EnumChildWindows(hwnd, do_control, 0)


def check_all():
    log_print("=" * 80)
    log_print('\t%s' % Product_Type_Name)
    log_print("=" * 80)
    extract_win_option()

    print(all_hwnd_TComboBox)
    print(all_hwnd_TRadioButton)
