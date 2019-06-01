import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread(r'D:\navagation\test\V%CZNK5VY63B7D5U99KGUD9.jpg', 0)


orb = cv2.ORB_create()


kp = orb.detect(img,None)


kp, des = orb.compute(img, kp)
cv2.Dr
img = cv2.drawKeypoints(img,kp,img,color=(0,255,0), flags=0)

cv2.imshow('p', img)

cv2.waitKey()
