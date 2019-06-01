import cv2
from camera1 import Camera
import numpy as np
import screeninfo
import mvsdk
from window import Window


'''

存的速度在25帧/s
main-1的作用是把医生自己做手术的场景录制下来，为了方便后来储存一屏二屏的标记，不录制成视频，改为存成一张张照片。
m的作用：m为True的时候开始存，m为False的时候不存  一开始调整位置可以不存，中间要调整的时候也可以不存。
n的作用：计数
imwrite保存的地址随意

'''


# 初始化相机
Cam = Camera()
# 初始化m,n m为False不存，调整好位置角度以后，按m开始存
m, n = False, 0
while 1:
    frame = Cam.run()
    cv2.flip(frame, 0, frame)
    cv2.imshow('just see see', frame)
    k = cv2.waitKey(10) & 0xFF
    if m:
        cv2.imwrite(r'C:\Users\Administrator\Desktop\image\%s.png' % n, frame)
        print('saving image_%s' % n)
        n += 1
    if k == ord('m'):
        m = not m
