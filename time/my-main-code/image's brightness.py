import matplotlib
import cv2
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# test
# image2 = np.zeros([600, 800, 3], np.uint8)
# print(len(image2[0]),len(image2))
# cv2.imshow('1',image2)
# cv2.waitKey()
# print(image)
# cv2.namedWindow('image',cv2.WINDOW_NORMAL)
# cv2.resizeWindow('image',800,600)
# cv2.imshow('image',image)
# cv2.waitKey()

#定义坐标轴
fig = plt.figure()
# ax1 = plt.axes(projection='3d')
ax2 = Axes3D(fig)

image =  cv2.imread(r'D:\teleguience\teleguidence\time\my-main-code\picture\4.jpg')
# image = np.zeros([600, 800, 3], np.uint8)
# image[:][:] = 255
# print(image)
b, g, r = cv2.split(image)
xd = np.arange(0, image.shape[1])
yd = np.arange(0, image.shape[0])
xd, yd = np.meshgrid(xd, yd)
zd = r
# print(g)
# print(g.shape)
ax2.scatter3D(xd,yd,zd, cmap='green',marker='.', s=50, label='')
plt.show()

