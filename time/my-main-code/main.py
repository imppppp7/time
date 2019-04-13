import cv2
import numpy as np
import screeninfo
import mvsdk
from window import Window
from camera1 import Camera


# 生成相机的实例化对象
# cam = Camera()

# 生成窗体对象
pro = Window('projector_1','projector_2')
pro.createwindow(1280, 800)
pro.movewindow(1)
pro.bindingwi((0, 255, 0), (255, 255, 255))

while 1:
    # frame = cam.run()
    frame = np.zeros([800, 1280, 3], np.uint8)
    frame = cv2.flip(frame, 0)
    frame = cv2.resize(frame, (1280, 800))
    pro.addimage(frame)
    pro.showimage()
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        pro.mode = not pro.mode
    if k == ord('q'):
        break
cv2.destroyAllWindows()


