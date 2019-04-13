import cv2
import numpy as np
import screeninfo
import mvsdk
from window import Window
from camera1 import Camera


# 生成相机的实例化对象
cam = Camera()
# 生成窗体对象
pro = Window('projector_1','projector_2')
# 前两个参数是第一个窗体，后两个是第二个窗体
pro.createwindow(1280, 800, 1280, 800)
# 连投影仪运行这句话，不连就注释掉，否则会报错 out of range
pro.movewindow(1)
pro.bindingwi((0, 255, 0), (255, 255, 255))
pro.nobiaotilan()

while 1:
    frame = cam.run()
    # 有相机的时候就把frame = np.zeros注释掉 打开cam = Camera()和frame = cam.run()
    frame = np.zeros([800, 1280, 3], np.uint8)
    frame = cv2.flip(frame, 0)
    frame = cv2.resize(frame, (1280, 800))
    pro.addimage(frame)

    # 前两个参数调大小，后两个参数调位置
    pro.showimage(800, 600, 10, 10)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        pro.mode = not pro.mode
    if k == ord('q'):
        break
cv2.destroyAllWindows()


