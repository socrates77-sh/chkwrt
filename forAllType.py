from mylib import *
import win32api
import win32gui
import win32con
import time
import os
# import struct

Product_Type_Name = ''  # 品名
Option_Win_Title = ''  # 配置Option的窗口标题

# 全局变量，遍历option窗口空间的序号
# index_of_control = 0

hwnd_main = 0  # 主窗口句柄
# hwnd_group_tool = 0  # 包含<配置芯片>按键的group句柄
hwnd_option_win = 0  # option窗口句柄
all_hwnd_TComboBox = []  # 所有option窗口中TComboBox（可见的）列表
all_hwnd_TRadioButton = []  # 所有option窗口中TRadioButton（可见的）列表
# serial_id = 0  # 一种选项的序号


def get_win_option_handle(option_title):
    """
    获取配置Option窗口的句柄
    :return: 返回句柄；不成功则返回0
    """
    # 逐级查找配置芯片Button的handle
    global hwnd_main
    global hwnd_group_tool
    hwnd_group_tool = win32gui.FindWindowEx(
        hwnd_main, 0, None, TOOL_GROUP_TEXT)

    # 点击配置芯片Button，打开Option窗口
    if click_button(hwnd_group_tool, CONFIG_BUTTON_TEXT):
        return win32gui.FindWindow(None, option_title)
    else:
        return False


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
    if win32gui.IsWindowVisible(hwnd):
        all_hwnd_TComboBox.append(hwnd)


def gather_all_TRadioButton(hwnd):
    '''
    将抓取到可见的TRadioButton的hwnd存到list中
    '''
    if win32gui.IsWindowVisible(hwnd):
        all_hwnd_TRadioButton.append(hwnd)


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
    #           (index_of_control, control_text, class_name), end='\n')

    # log_print('[%02d](class)%-20s(text)%s' %
    #           (0, control_text, class_name), end='\n')

    if class_name == 'TRadioButton':
        gather_all_TRadioButton(hwnd)
    elif class_name == 'TComboBox':
        gather_all_TComBox(hwnd)
    else:
        # log_print('')
        pass

    # index_of_control += 1


def extract_win_option():
    """
    提取Option窗口的信息
    :return:
    """

    # 遍历Option窗口的所有控件
    # global index_of_control
    # index_of_control = 0
    # hwnd_main = win32gui.FindWindow(None, 'EZPro100')
    global hwnd_option_win
    global all_hwnd_TComboBox
    global all_hwnd_TRadioButton
    hwnd_option_win = get_win_option_handle(Option_Win_Title)
    if not hwnd_option_win:
        print('Not find option window')
        exit(3)
    all_hwnd_TComboBox = []
    all_hwnd_TRadioButton = []
    win32gui.EnumChildWindows(hwnd_option_win, do_control, 0)


def click_radio(hwnd):
    """
    按下一个Radio的操作
    :param hwnd: Radio的handle
    :return: None
    """
    win32api.SendMessage(hwnd, win32con.BM_SETSTATE, win32con.BST_CHECKED, 0)
    win32gui.SendMessage(hwnd, win32con.WM_SETFOCUS, 0, 0)
    time.sleep(WAIT_SECOND / 3)
    win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(WAIT_SECOND / 3)
    win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    time.sleep(WAIT_SECOND / 3)


def click_button(hwnd_parent, button_text):
    """
    按下一个按钮的操作
    :param hwnd_parent: 按钮父窗口的handle
    :param button_text: 按钮的text
    :return: 成功则返回True, 否则返回False
    """
    hwnd_bt = win32gui.FindWindowEx(hwnd_parent, 0, None, button_text)
    if hwnd_bt != 0:
        win32api.PostMessage(hwnd_bt, win32con.BM_CLICK, 0, 0)
        time.sleep(WAIT_SECOND)
        return True
    else:
        return False


def click_menu(hwnd, n_sub_pos, n_item_pos):
    """
    点击菜单项
    :param hwin: 菜单所在窗口句柄
    :param n_sub_pos: 子菜单序号，0起始
    :param n_item_pos: 菜单项序号，0起始
    :return: None
    """
    h_menu = win32gui.GetMenu(hwnd)
    h_submenu = win32gui.GetSubMenu(h_menu, n_sub_pos)
    h_menuitem = win32gui.GetMenuItemID(h_submenu, n_item_pos)
    # print(h_menu, h_submenu, h_menuitem)
    win32gui.BringWindowToTop(hwnd)
    win32gui.PostMessage(hwnd, win32con.WM_COMMAND, h_menuitem)


def open_wrt_file(file_name):
    """
    点击菜单方式打开Open对话框，并打开指定的WRT文件
    :param hwnd_main: 菜单所在窗口的句柄
    :param file_name: WRT文件名，含路径
    :return: 如文件不存在，则返回False；否则返回Ture
    """
    global hwnd_main
    if not os.path.exists(file_name):
        print("Error: File %s not found!" % file_name)
        return False
    else:
        click_menu(hwnd_main, 0, 0)  # 点击“Open”菜单
        time.sleep(WAIT_SECOND)
        h_dlg_open = win32gui.FindWindow(None, "打开")
        h_txt_filename = win32gui.GetDlgItem(h_dlg_open, 0x47c)
        # 填写filename的值
        win32gui.SendMessage(h_txt_filename, win32con.WM_SETTEXT, 0, file_name)
        click_button(h_dlg_open, "打开(&O)")  # 点击Open按钮
        log_print("\tload ... %s" % file_name)
        return True


def save_wrt_file(file_name):
    """
    点击菜单方式打开Save对话框，并保存为指定的WRT文件
    :param file_name: WRT文件名，含路径
    :return: 如路径不存在，则返回False；否则返回Ture
    """
    global hwnd_main
    path_name = os.path.dirname(file_name)
    if not os.path.exists(path_name):
        print("Error: Path %s not found!" % path_name)
        return False
    else:
        # 文件存在则先删除，保证更新
        if os.path.exists(file_name):
            os.remove(file_name)
        click_menu(hwnd_main, 0, 1)  # 点击“Save as”菜单
        time.sleep(WAIT_SECOND)
        h_dlg_save = win32gui.FindWindow(None, "另存为")
        h_txt_filename = win32gui.GetDlgItem(
            h_dlg_save, 0x47c)  # 以ID方式取得filename控件（Edit）的句柄
        file_name_wo_ext = file_name.split('.')[0]
        # 填写filename的值
        win32gui.SendMessage(
            h_txt_filename, win32con.WM_SETTEXT, 0, file_name_wo_ext)
        click_button(h_dlg_save, "保存(&S)")  # 点击Save按钮
        log_print("\tsave ... %s" % file_name)
        return True


def compare_file(fn_a, fn_b):
    """
    以bin的方式比较两个文件是否一致
    :param fn_a, fn_b: 两个文件名，含路径
    :return: 文件相同，则返回True；否则返回False
    """
    try:
        f_a = open(fn_a, 'rb')
        data_a = f_a.read()
        size_a = f_a.tell()
        f_a.close()
        f_b = open(fn_b, 'rb')
        data_b = f_b.read()
        size_b = f_b.tell()
        f_b.close()
    except Exception as e:
        print(e)

    if size_a != size_b:
        return False

    da_a = bytearray(data_a)
    da_b = bytearray(data_b)
    for i in range(0, size_a):
        if da_a[i] != da_b[i]:
            return False

    return True


def do_radio_item(radio_id, serial_id):
    '''
    完成一个radio选项的所有保存、载入、比较
    :return: 比较正确，则返回True；否则返回False
    '''
    global all_hwnd_TRadioButton

    log_print("ITEM No. %d" % serial_id)

    # open option window, select one radio, click ok, save wrt
    extract_win_option()
    log_print("\topen option window")
    hwnd_radio = all_hwnd_TRadioButton[radio_id]
    click_radio(hwnd_radio)
    radio_text = win32gui.GetWindowText(hwnd_radio)
    log_print("\tselect: Radio[%d] %s" % (radio_id, radio_text))
    click_button(hwnd_option_win, OPTION_OK_BUTTON_TEXT)
    log_print("\tclick ok button")
    rep_path = os.path.join(os.path.curdir, "rep")
    fn_a = os.path.join(rep_path, "%s_%03d_A.wrt" %
                        (Product_Type_Name, serial_id))
    fn_a_abs = os.path.abspath(fn_a)
    save_wrt_file(fn_a_abs)

    # load wrt_a, open option window, click ok, save wrt_b
    open_wrt_file(fn_a_abs)
    extract_win_option()
    log_print("\topen option window")
    click_button(hwnd_option_win, OPTION_OK_BUTTON_TEXT)
    log_print("\tclick ok button")
    fn_b = os.path.join(rep_path, "%s_%03d_B.wrt" %
                        (Product_Type_Name, serial_id))
    fn_b_abs = os.path.abspath(fn_b)
    save_wrt_file(fn_b_abs)
    cmp_result = compare_file(fn_a_abs, fn_b_abs)
    log_print("\tcompare: %s <-> %s" %
              (os.path.basename(fn_a_abs), os.path.basename(fn_b_abs)))
    if cmp_result:
        log_print("[Pass]")
        return True
    else:
        log_print("[Fail]")
        return False


def check_all():
    global hwnd_main
    global hwnd_option_win

    log_print("=" * 80)
    log_print(Product_Type_Name)
    log_print("=" * 80)

    hwnd_main = win32gui.FindWindow(None, EZPRO_TITLE)
    if not hwnd_main:
        print('Not find main window')
        exit(2)

    # 获取radio和combo的数量，由于每次打开相关的hwnd会改变，所以实际不用list的内容
    extract_win_option()
    n_radio = len(all_hwnd_TRadioButton)
    n_combo = len(all_hwnd_TComboBox)
    click_button(hwnd_option_win, OPTION_CANCEL_BUTTON_TEXT)

    if not os.path.exists(os.path.join(os.path.curdir, "rep")):
        os.makedirs(os.path.join(os.path.curdir, "rep"))

    count_pass = 0
    count_fail = 0
    serial_number = 1
    # for i in range(0, n_radio):
    for i in range(0, 2):
        if do_radio_item(i, serial_number):
            count_pass += 1
        else:
            count_fail += 1
        serial_number = serial_number + 1

    log_print("=" * 80)
    log_print("Summary")
    log_print("\tPass: %d\n\tFail: %d" % (count_pass, count_fail))
    log_print("=" * 80)
