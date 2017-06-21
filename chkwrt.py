"""主程序入口"""


from mylib import *
# from forAllType import *
import forAllType
import datetime

VERSION = 'v0.1'


def check_process():
    # 判断EZPro100是否运行，且只有一个进程
    _process_name = EZPRO_TITLE + '.exe'
    process_num = get_process_count(_process_name)
    if process_num == 0:
        print('ERROR: %s is not running!' % EZPRO_TITLE)
        exit(-1)
    elif process_num > 1:
        print('ERROR: More than one %s are running!' % EZPRO_TITLE)
        exit(-2)
    else:
        print("Found %s running!\n" % EZPRO_TITLE)


def main():
    check_process()

    # 打印时间到LOG文件
    log_print('chkwrt (%s) %s'
              % (VERSION, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    forAllType.Product_Type_Name = "MC30P6080"
    forAllType.Option_Win_Title = "配置 %s" % forAllType.Product_Type_Name
    forAllType.check_all()

    f_log.close()

if __name__ == '__main__':
    main()
