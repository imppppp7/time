import cv2
img = cv2.imread(r'D:\teleguience\teleguidence\time\piuture\1.png')
# img = cv2.GaussianBlur(img,(5,5),5)

# 转换空间到hsv, 对v通道直方图均衡化

img_2 = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(img_2)
# cv2.imshow('1',h)
# cv2.waitKey()
v_2 = cv2.equalizeHist(v)
img_3 = cv2.merge([h,s,v_2])
img_4 = cv2.cvtColor(img_3,cv2.COLOR_HSV2BGR)
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.imshow('image',img_4)
cv2.waitKey()
cv2.fas