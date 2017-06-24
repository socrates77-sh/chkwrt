from mylib import *
import win32api
import win32gui
import win32con
import time


class forAllType:
    def __init__(self, type_name, option_title):
        self.type_name = type_name
        self.option_title = option_title
        self.all_hwnd_TComboBox = []
        self.all_hwnd_TRadioButton = []

    def get_win_option_handle(self):
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
            return win32gui.FindWindow(None, self.option_title)
        else:
            return 0

    def gather_all_TComBox(self, hwnd):
        '''
        将抓取到可见的TComBox的hwnd存到list中
        '''
        if(win32gui.IsWindowVisible(hwnd)):
            all_hwnd_TComboBox.append(hwnd)

    def gather_all_TRadioButton(self, hwnd):
        '''
        将抓取到可见的TRadioButton的hwnd存到list中
        '''
        if(win32gui.IsWindowVisible(hwnd)):
            all_hwnd_TRadioButton.append(hwnd)

    # @staticmethod
    def do_control(hwnd, lparam):
        """
        EnumChildWindows需要的EnumWindowsCallback函数
        :param hwnd: EnumChildWindows获取的hwnd
        :param lparam: EnumChildWindows获取的lparam
        :return: None
        """

        # 获取空间的text和class_name
        # global index_of_control
        control_text = win32gui.GetWindowText(hwnd)
        class_name = win32gui.GetClassName(hwnd)
        # log_print('[%02d](class)%-20s(text)%s' %
        #           (index_of_control, control_text, class_name), end='')

        if class_name == 'TRadioButton':
            self.gather_all_TRadioButton(hwnd)
        elif class_name == 'TComboBox':
            self.gather_all_TComBox(hwnd)
        else:
            # log_print('')
            pass
        # index_of_control += 1

    def extract_win_option(self):
        """
        提取Option窗口的信息
        :return:
        """
        hwnd = self.get_win_option_handle()

        if(hwnd == 0):
            print('Not find option window')
            exit(2)

        # 遍历Option窗口的所有控件
        # global index_of_control
        # index_of_control = 0
        win32gui.EnumChildWindows(hwnd, self.do_control, 0)
