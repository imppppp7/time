import cv2
import numpy as np
from copy import deepcopy
'''
可以用函数嵌套来代替global
def y1(x1)
    def y2(x2)
        x1+x2
'''
drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = 1,1

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix, iy, drawing, mode
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv2.circle(img, (x, y), 4, (0, 255, 0), -1)
            else:
                img[y - 25:y + 25, x - 25:x + 25, :] = img_copy[y - 25:y + 25, x - 25:x + 25, :]

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
    ix, iy = x, y
    # print('函数1的x,y',[ix,iy])
    copy_circle(event,ix,iy,flags,param)

def copy_circle(event, x2, y2, flags, param):
        global drawing, mode
        x2 = ix
        y2 = iy
        # print('hanshu2',[x2, y2])

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            # print('Yunxing1')
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                if mode == True:
                    cv2.circle(img2, (x2, y2), 3, (255, 255, 255), -1)
                    # print('Yunxing2')
                else:
                    img2[y2 - 25:y2 + 25, x2 - 25:x2 + 25, :] = img2_copy[y2 - 25:y2 + 25, x2 - 25:x2 + 25, :]

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False

        # if mode == True:
        #     cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        # else:
        #     img[y - 5:y + 5, x - 5:x + 5, :] = img_copy[y - 5:y + 5, x - 5:x + 5, :]

img = cv2.imread(r'D:\teleguience\teleguidence\time\mode.png')
# print(img.shape)
img_copy = deepcopy(img)
img2 = np.zeros((1024,1920,3), np.uint8)
img2_copy = deepcopy(img2)
# cv2.namedWindow('image_cp',cv2.WINDOW_NORMAL)
# cv2.resizeWindow('image_cp',640,480)
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',640,480)
cv2.namedWindow('image2',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image2',640,480)
# cv2.namedWindow('image2_cp',cv2.WINDOW_NORMAL)
# cv2.resizeWindow('image2_cp',640,480)
cv2.setMouseCallback('image',draw_circle)
cv2.setMouseCallback('image2',copy_circle)

while(1):
    cv2.imshow('image',img)
    # cv2.imshow('image_cp',img_copy)
    cv2.imshow('image2',img2)
    # cv2.imshow('image2_cp', img2)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == ord('q'):
        break
cv2.destroyAllWindows()
