import cv2
import numpy as np
# pycharm 配库 将project interpreter 设置成 conda 环境 exsiting environment
# 然后在下载各种库 下载完等一会


def color_seperate(image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   #对目标图像进行色彩空间转换
        # lower_bgr = np.array([255, 255, 0])
        lower_bgr = np.array([60, 20, 125])  #设定蓝色下限
        # upper_bgr = np.array([255, 255, 0])
        upper_bgr = np.array([87, 38, 150])#设定蓝色上限
        mask = cv2.inRange(image, lowerb=lower_bgr, upperb=upper_bgr)  #依据设定的上下限对目标图像进行二值化转换
        dst = cv2.bitwise_and(src, src, mask=mask)    #将二值化图像与原图进行“与”操作；实际是提取前两个frame 的“与”结果，然后输出mask 为1的部分
        cv2.namedWindow('result',cv2.WINDOW_NORMAL)
        cv2.imshow('result', dst)   #输出

src = cv2.imread(r'C:\project\teleguidence\time\red.png')   #导入目标图像，获取图像信息
color_seperate(src)
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.imshow('image', src)
cv2.waitKey(0)
cv2.destroyAllWindows()
