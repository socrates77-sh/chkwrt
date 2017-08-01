"""主程序入口"""


from mylib import *
# from forAllType import *
# import forMC30P6080
import forAllType
import datetime

VERSION = 'v0.3'

print("使用说明：")
print("(1) 已打开一个EZPRO100软件")
print("(2) 已选择要测试的型号")
print("(3) 已关闭配置窗口")
print("")

product = input("请输入型号: ")

print("\n")

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
log_print('chkwrt (%s) %s' %
          (VERSION, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

product = product.strip().upper()
forAllType.Product_Type_Name = product
forAllType.Option_Win_Title = '配置 %s' % product
forAllType.check_all()
f_log.close()

print("请查看result.log文件及rep目录")

anykey = input("press any key to exit")
