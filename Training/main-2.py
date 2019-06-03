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
运行完main-1后运行main-2,main-1.main-2是给医生录视频用的，main-3是手术训练的时候看的
1.让医生看他自己操作时候的视频,并且在看的过程中做一些标记
2.n的作用：计数 使得各个图片一一对应
3.两个cv2.imwrite ：pro.image3是一屏的标记 pro.image5是二屏的标记 这里几个参数是调同轴的，需要提前把程序中的参数调好，再在让医生来
4.地址要注意保持一致 image3 image5分别保持一致
功能：
1.m的作用是在画线和擦线之间切换
2.空格的作用是在某一帧暂停 按一下暂停 再按一下继续播放下一帧
3.z的作用是跳跃到某一段去
缺陷：
1.程序里画了标记，该图就会保存下来，擦除只能让下面的图没有标记。就像拍一个视频一样，只要记录下来了，就没法重来了，所以如果是医生失误画错了，就重启程序重头再来

'''


# 每次运行程序之前都会先把这个文件夹里的东西清空，防止上一次运行会残留文件，但是第一次运行程序之前必须要创建一个空的文件夹
# 删除文件夹
shutil.rmtree(r'C:\Users\Administrator\Desktop\image3')
shutil.rmtree(r'C:\Users\Administrator\Desktop\image5')
shutil.rmtree(r'C:\Users\Administrator\Desktop\recording')
# 创建空的文件夹
os.mkdir(r'C:\Users\Administrator\Desktop\image3')
os.mkdir(r'C:\Users\Administrator\Desktop\image5')
os.mkdir(r'C:\Users\Administrator\Desktop\recording')

# 生成窗体对象
pro = Window('projector_1', 'projector_2', 800, 600)
pro.createwindow(1280, 800)
# 连投影仪运行这句话，不连就把1改成0，否则会报错 out of range
pro.movewindow(1)
# 前两个参数是一屏二屏标记的颜色，第三个参数是标记的宽度，最后两个参数 要和生成窗体对象的最后两个参数保持一致，如果想要二屏标记也是绿色就把（255,255,255）改成（0,255,0）
pro.bindingwi((0, 255, 0), (255, 255, 255), 3, 800, 600)
pro.nobiaotilan()
# n用来计数
n = 0
# 加个trackbar方便快进或快退到某一位置


def nothing(x):
    pass


cv2.createTrackbar('z', 'projector_1', 0, 255, nothing)
while 1:
    frame = cv2.imread(r'C:\Users\Administrator\Desktop\image1\%s.png' % n)
    pro.addimage(frame)
    # 调同轴前两个参数调大小，后两个参数调位置,第五个参数调框的宽度
    pro.changeimage(550, 400, 245, 190, 5)
    pro.showimage()
    # 保存一屏的标记图
    cv2.imwrite(r'C:\Users\Administrator\Desktop\image3\%s.png' % n, pro.image3)
    # 保存二屏的标记图
    cv2.imwrite(r'C:\Users\Administrator\Desktop\image5\%s.png' % n, pro.image5)
    # 保存音频
    path1 = r'C:\Users\Administrator\Desktop\recording\%s.wav' % n
    time = 0.01
    Audio.record_audio(time, path1)
    z = cv2.getTrackbarPos('z', 'projector_1')
    print('n=', n)
    n += 1
    # waitkey的时间决定了播放的帧率 waitkey 时间越短，放的越快
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        pro.mode = not pro.mode
    if k == ord(' '):
        cv2.waitKey()
    if k == ord('z'):
        # n = int(input())
        n = z

