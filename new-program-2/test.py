# import cv2
#
# img = cv2.imread(r'D:\navagation\time\piuture\IMG_3606.JPG')
# IMG = cv2.flip(img, 1)
# cv2.circle(img, (100, 500), 10, (255, 0, 0),-1)
# cv2.namedWindow('1',cv2.WINDOW_NORMAL)
# cv2.imshow('1', img)
# cv2.namedWindow('2',cv2.WINDOW_NORMAL)
# cv2.imshow('2', IMG)
# cv2.waitKey()
# import copy
# list1 = [0, 1]
# list1.append(2)
# print(list1[-1])
# list2 = list1[:]
# list1[0] = 10
# print(list1, list2)
import cv2
#
img = cv2.imread("image1.BMP")
roi = cv2.selectROI(windowName="roi", img=img, showCrosshair=True, fromCenter=False)
x, y, w, h = roi
print(roi)
cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 255), thickness=2)
cv2.imshow("roi", img)
cv2.waitKey(0)