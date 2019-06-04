import cv2
from camera1 import Camera
import numpy as np
import screeninfo
import mvsdk
import os
from window import Window
import shutil
import os
from Audio import Audio

'''
解释：
空格： 暂停
调waitkey的时间，可以调视频播放的快慢，waitkey 时间越短，放的越快
'''


# 生成窗体对象
pro = Window('projector_1', 'projector_2', 800, 600)
pro.createwindow(1280, 800)
# 连投影仪运行这句话，不连就把1改成0，否则会报错 out of range
pro.movewindow(1)
# 前两个参数是一屏二屏标记的颜色，第三个参数是标记的宽度，最后两个参数 要和生成窗体对象的最后两个参数保持一致，如果想要二屏标记也是绿色就把（255,255,255）改成（0,255,0）
# pro.bindingwi((0, 255, 0), (255, 255, 255), 3, 800, 600)
pro.nobiaotilan()
# n用来计数
n = 0
# 加个trackbar方便快进或快退到某一位置


def nothing(x):
    pass


cv2.createTrackbar('z', 'projector_1', 0, 255, nothing)
while 1:
    frame = cv2.imread(r'C:\Users\Administrator\Desktop\image1\%s.png' % n)
    pro.image3 = cv2.imread(r'C:\Users\Administrator\Desktop\image3\%s.png' % n)
    pro.image5 = cv2.imread(r'C:\Users\Administrator\Desktop\image5\%s.png' % n)
    pro.addimage(frame)
    pro.showimage()
    # path2 = r'C:\Users\Administrator\Desktop\recording\%s.wav' % n
    # Audio.play_audio(path2)
    # waitkey的时间决定了播放的帧率 waitkey 时间越短，放的越快
    print('n=', n)
    z = cv2.getTrackbarPos('z', 'projector_1')
    n += 1
    k = cv2.waitKey(1) & 0xFF
    if k == ord(' '):
        cv2.waitKey()
    if k == ord('z'):
        # n = int(input())
        n = z
    # 修改读哪个音频
    if n == 55 or n == 74:
        path2 = r'C:\Users\Administrator\Desktop\recording\%s.wav' % n
        Audio.play_audio(path2)
