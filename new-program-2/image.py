import cv2
import numpy as np
import screeninfo
import mvsdk
from window import Window
from camera1 import Camera


class Image:
    def __init__(self, width, height):
        # 实例化相机
        self.cam = Camera()
        self.n = 0
        self.image = np.zeros([height, width, 3], np.uint8)
        self.image1 = np.zeros([height, width, 3], np.uint8)

    def enhancebri(self, m):
        self.n = self.n + 1
        frame = self.cam.run()
        frame1 = cv2.flip(frame, 1)
        # frame = cv2.resize(frame, (800, 600))
        # frame1 = cv2.GaussianBlur(frame1, (5, 5), 1.5)
        self.image = cv2.add(frame1, self.image)
        if self.n % m == 0:
            self.n = 0
            self.image1 = self.image
            self.image = np.zeros([600, 800, 3], np.uint8)
            return self.image1
        print('self.n', self.n)

    def closecamera(self):
        mvsdk.CameraUnInit(self.cam.hCamera)

