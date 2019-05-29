import numpy as np
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import cv2
import numpy as np
from scipy import signal,ndimage
import time
import datetime

class Thread(QThread):
    #图片改变信号
    first_computation_flag = 1
    computation_flag = 0
    computation_finish_flag = 0

    camera_height = 2748
    camera_width = 3664
    laserimage_height = 960
    laserimage_width = 1280

    laser_computation_finish = pyqtSignal(QImage, np.ndarray, np.ndarray)
    img = QImage()
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        #截图框
        self.orignX = 0
        self.orignY = 0
        self.endX = 0
        self.endY = 0
        self.startPlotFlag = 0
        self.averageV = 0
        self.averageV = np.float64(self.averageV)

        self.plotdata = np.empty(0)
    def run(self):
        print("start computation thread")
        while True:
            if self.computation_flag:
                print("start computation ")
                mat = self.convertQImageToMat(self.img)
                print("start computation ", mat.shape)
                # mat = mat[0:480 ,0:640]
                print("computation  finished")
                laser, xVals, yVals  = self.laser_posess(mat, 5)

                mat_array = np.uint8(laser)

                mat_array = cv2.applyColorMap(mat_array, cv2.COLORMAP_JET)
                mat_array = cv2.cvtColor(mat_array, cv2.COLOR_BGR2RGB)

                # 调用 imshow显示
                # cv2.namedWindow("preview")
                # cv2.imshow("preview", mat_array)
                # cv2.imwrite('111.jpg',mat_array)
                laser_qimage = QImage(mat_array.data, mat_array.shape[1], mat_array.shape[0],
                                      QImage.Format_RGB888)  # Format_RGB16格式还需要再看看

                # print(type(xVals))
                # print(type(yVals))
                print("debug1")
                self.laser_computation_finish.emit(laser_qimage, xVals, self.plotdata)
                print('test')
                self.computation_flag = 0
                # self.computation_finish_flag = 1
    def receive_image(self,p):
        #第一次强制执行
        print("recevie image")
        # if self.first_computation_flag:
        #
        #     self.img = p
        #     print("first computation image")
        #     self.computation_flag = 1
        #     self.first_computation_flag = 0
        if (self.computation_flag == 0):
            self.img = p
            self.computation_flag = 1

        ##激光散斑处理
    def getPlotEdge(self, ox, oy, ex, ey):
        self.orignX = ox
        self.orignY = oy
        self.endX = ex
        self.endY = ey
        self.startPlotFlag = 1
        print("getPlotEdge")

    def laser_posess(self, imarray, wsize):
            posess_start = datetime.datetime.now()
            # imarray = cv2.cvtColor(imarray, cv2.COLOR_BGR2GRAY)
            # print(imarray.shape)
            print('start posess')
            imarray1 = imarray
            imarray1 = imarray.reshape(self.laserimage_height, self.laserimage_width)
            imarray1 = np.array(imarray1).astype(float)
            immean = ndimage.uniform_filter(imarray1, size=wsize)
            im2mean = ndimage.uniform_filter(np.square(imarray1), size=wsize)
            imcontrast = np.sqrt(abs(im2mean - np.square(immean)) / np.square(immean))
            # img_marker = imcontrast[0:20, 0:20]
            # immean_marker = np.mean(img_marker)
            # print(immean_marker)
            # imcontrast = imcontrast + immean_marker
            temp = 2 * np.square(imcontrast)
            result = np.real((1 + np.sqrt(1 - temp)) / temp)
            T1 = 0.0015
            v = 1000 * ((780 * 1e-9) / (2 * np.pi * T1)) * result
            xVals = np.linspace(0, 800, 801)
            bins = xVals.tolist()
            distribution = np.histogram(v, bins=bins)
            yVals = distribution[0]
            print('speckle computation finished')
            imcontrast_show = v*3  # 把（0，1）to （0，255）

            if(self.startPlotFlag == 1):
                print("STATR PLOT")
                self.averageV = np.average(v[self.orignX:self.endX, self.orignY:self.endY])
                self.plotdata = np.append(self.plotdata, self.averageV)
                print('average blood', type(self.averageV))

            # print(np.max(imcontrast_show))
            # print(np.min(imcontrast_show))
            # print(imcontrast_show.shape)
            # print(imcontrast_show.dtype)  # 图像类型
            imcontrast_show = np.array(imcontrast_show).astype(int)
            imcontrast_show = imcontrast_show.reshape(self.laserimage_height, self.laserimage_width, 1)
            print('imcontrast', imcontrast_show.shape)
            # imcontrast_show = np.transpose(imcontrast_show, (1, 0, 2)).copy()

            posess_end = datetime.datetime.now()
            print('laser_posess finished and time=', posess_end - posess_start)

            return imcontrast_show, xVals, yVals
    def convertQImageToMat(self,p):
        '''  Converts a QImage into an opencv MAT format  '''
        convert_start = datetime.datetime.now()
        p = p.convertToFormat(3)
        ptr = p.bits()
        ptr.setsize(p.byteCount())
        arr = np.array(ptr).reshape(p.height(), p.width(), 1)
        convert_end = datetime.datetime.now()
        print("convertQImageToMat Finished and time =", convert_end - convert_start)
        return arr

