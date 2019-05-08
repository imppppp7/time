import cv2

img = cv2.imread(r'D:\navagation\time\piuture\IMG_3606.JPG')
IMG = cv2.flip(img, 1)
cv2.circle(img, (100, 500), 10, (255, 0, 0),-1)
cv2.namedWindow('1',cv2.WINDOW_NORMAL)
cv2.imshow('1', img)
cv2.namedWindow('2',cv2.WINDOW_NORMAL)
cv2.imshow('2', IMG)
cv2.waitKey()