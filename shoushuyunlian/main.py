import cv2
import numpy as np
import screeninfo
import mvsdk
from window import Window
from camera1 import Camera
from image import Image


# 生成窗体对象
pro = Window('projector_1', 'projector_2', 800, 600)
# 生成相机图像对象,width, height要和相机获取的图像保持一致
# Img = Image(800, 600)
# 前两个参数是第一个窗体，后两个是第二个窗体
pro.createwindow(1280, 800)
# 连投影仪运行这句话，不连就把1改成0，否则会报错 out of range
pro.movewindow(1)

# 前两个参数是一屏二屏标记的颜色，第三个参数是标记的宽度，最后两个参数 要和生成窗体对象的最后两个参数保持一致，如果想要二屏标记也是绿色就把（255,255,255）改成（0,255,0）
pro.bindingwi((0, 255, 0), (255, 255, 255), 3, 800, 600)
pro.nobiaotilan()
# 假设两个参数m,n.  n是为了计数 m是相机拍到的几张图混合在一起
n, m = 0, 6
# 不开相机的时候，拿这个图当相机的图
frame = cv2.imread(r'D:\navagation\time\piuture\IMG_3606.jpg')
frame = cv2.resize(frame, (800, 600))
while 1:
    # frame = np.zeros([800, 1280, 3], np.uint8)
    n = n + 1
    # 由于相机拍到的图像左右反转，所以Img.enhancebri(m)里面左右翻转了图像
    # frame = Img.enhancebri(m)
    if n % m == 0:
        n = 0
        # 给一屏幕中间加个十字线 299：300 399：400
        frame[299:300, 0:799] = [255, 255, 255]
        frame[0:599, 399:400] = [255, 255, 255]
        pro.addimage(frame)
        # 前两个参数调大小，后两个参数调位置,第五个参数调框的宽度
        pro.changeimage(550, 400, 245, 190, 5)
        pro.showimage()
    print('n', n)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        pro.mode = not pro.mode
    # if k == ord('q'):
        # 关闭相机
        # break
        # Img.closecamera()
        # cv2.destroyAllWindows()
