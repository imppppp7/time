from savetime import Savetime
import cv2
import xlwt
import datetime
import PyHook3
import pythoncom

# 调用程序一直记录时间
record = Savetime('TEST','1')
record.hook()


# 获取一次时间
# while 1:
#     record.write_time()
#     cv2.waitKey(2000)
