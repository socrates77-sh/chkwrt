"""主程序入口"""

# !/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zwr'

from mylib import *
import forMC30P6060
import datetime

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

# 打印时间到LOG文件
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), file=f_log)

forMC30P6060.check_all()

f_log.close()