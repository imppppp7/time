import sys
from PyQt5.QtWidgets import QApplication, QWidget,QSlider, QRubberBand
from laserspeckle_process.camera import Ui_widget
from PyQt5.QtCore import Qt, pyqtSignal,QPoint, QRect, QSize
from PyQt5.QtGui import QPixmap, QColor, QImage, qRgb
from laserspeckle_process import camera_thread
import numpy as np
from laserspeckle_process import  computation_thread
import pyqtgraph as pg

from matplotlib import cm,figure,pyplot

import cv2
from scipy import signal,ndimage
from PIL import Image
import datetime

class App(QWidget):

    #几个传递值的信号
    ExposuretimeChangedValue = pyqtSignal(int)
    GainChangedValue = pyqtSignal(int)
    plotBlood = pyqtSignal(int, int, int, int )
    #绘图
    laser_computation= pyqtSignal(QImage)
    camera_height = 2748
    camera_width = 3664
    laserimage_height = 2748
    laserimage_width = 3664
    win = pg.GraphicsWindow(title="v distribution")
    win.resize(500, 300)
    win.setWindowTitle('blood perfusion')
    p = win.addPlot(title='blood perfusion')
    p.setLabel(axis='left', text='v')
    p.setLabel(axis='bottom', text='number')
    p.setRange(yRange=[0 , 150], padding=0)

    curve = p.plot(pen='y')


    def __init__(self):
            super(App,self).__init__()
            self.ui = Ui_widget()
            self.ui.setupUi(self)
            self.title = 'PyQt5 Video'

            self.initUI()
            self.origin = QPoint()
            self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)

            self.originX = 0
            self.originY = 0
            self.endX = 0
            self.endY = 0

            self.plotFlag = 0
            self.plotdata = np.empty(0)

            self.plotdata_v1 = np.empty(0)
            self.plotdata_v1_flag = 0


    def initUI(self):
            #相机线程
            th = camera_thread.Thread(self)
            #计算线程
            computation_th = computation_thread.Thread(self)
            self.laser_computation.connect(lambda p: computation_th.receive_image(p))  # 测试用
            computation_th.laser_computation_finish.connect(lambda p, x, y: self.setLaserImage(p, x, y))
            th.changePixmap.connect(lambda p: self.setPixMap(p))  # 将changePixmap 函数与setPixMap 函数 联系起来
            th.laser_posess.connect(lambda p: self.get_under_posess_image(p))#
            #显示初始值
            self.ui.lineEdit_gain.setText(str(th.Gain))
            self.ui.lineEdit_exposuretime.setText(str(th.Exposuretime))
            #发送图片
            #截取图片
            self.ui.label_CaptureFrame.clicked.connect(th.capturePicture)
            #滑动条修改曝光时间
            self.ui.horizontalSlider_SetExposure.setTickPosition(QSlider.TicksBelow)
            self.ui.horizontalSlider_SetExposure.valueChanged.connect(self.on_changed_ExposureTime)
            self.ui.horizontalSlider_SetExposure.valueChanged.connect(th.CameraSettingChanged)
            self.ExposuretimeChangedValue.connect(lambda value: th.CameraSettingExposuretime(value))
            #滑动条修改帧率
            self.ui.horizontalSlider_Setfps.valueChanged.connect(th.CameraSettingChanged)
            #滑动条修改增益
            self.ui.horizontalSlider_SetGain.setTickPosition(QSlider.TicksBelow)
            self.ui.horizontalSlider_SetGain.valueChanged.connect(th.CameraSettingChanged)
            self.ui.horizontalSlider_SetGain.valueChanged.connect(self.on_changed_Gain)
            self.GainChangedValue.connect(lambda value: th.CameraSettingExposuretime(value))
            self.ui.label_OpenCamera.setMouseTracking(True)
            #plot按钮功能
            self.ui.label_PlotBloodFlow.clicked.connect(self.PlotBloodFlow)

            #不同流速血流计算功能
            self.ui.pushButton_v1.setCheckable(True)
            self.ui.pushButton_v1.toggled.connect(self.changeV1Flag)

            #还差保持路径、截取间隔、还有截取时间
            #开启线程
            #画图信号
            self.plotBlood.connect(lambda ox, oy, ex, ey: computation_th.getPlotEdge(ox, oy, ex, ey))
            th.start()
            computation_th.start()
            print("init gui finish")

    #修改相机曝光时间
    def on_changed_ExposureTime(self, value):

        Exposuretime = self.ui.horizontalSlider_SetExposure.value()
        self.ui.lineEdit_exposuretime.setText(str(Exposuretime))
        print(Exposuretime)
        # self.plotdata = np.append(self.plotdata, Exposuretime)
        # print(self.plotdata)
        # self.curve.setData(self.plotdata)
        self.ExposuretimeChangedValue.emit(Exposuretime)
    #修改相机增益
    def on_changed_Gain(self, value):
        Gain = self.ui.horizontalSlider_SetGain.value()
        self.ui.lineEdit_gain.setText(str(Gain))
        print(Gain)
        self.GainChangedValue.emit(Gain)
    #显示拍摄图片
    def setPixMap(self, p):
        p = QPixmap.fromImage(p)
        p = p.scaled(640, 480, Qt.KeepAspectRatio)
        self.ui.label_VideoDisplay.setPixmap(p)
    #显示激光散斑图像
    def get_under_posess_image(self,p):
        print("get under posess image")
        under_posess_image = p
        print(type(p))
        self.laser_computation.emit(under_posess_image)
        print("send image to thread to possess")
# 鼠标响应事件，用来画圈求均值
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.originX = event.x()
            self.originY = event.y()
            print(self.originX, self.originY)
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endX = event.x()
            self.endY = event.y()
            print(self.endX, self.endY)
            # self.rubberBand.hide()
            #画完之后，获取区域，开始画图
            print("change the plotflag")
            labelOrignX = self.originX - self.ui.label_laserdisplay.x()
            print(labelOrignX)
            labelOrignY = self.originY - self.ui.label_laserdisplay.y()
            labelEndX = self.endX - self.ui.label_laserdisplay.x()
            labelEndY = self.endY - self.ui.label_laserdisplay.y()
            print(labelOrignX,labelOrignY, labelEndX, labelEndY)
            self.plotBlood.emit(labelOrignX, labelOrignY, labelEndX, labelEndY)
            self.plotFlag = 1
            print("change the plotflag")
    # def PlotBloodFlow(self):
    #     labelOrignX = self.originX - self.ui.label_laserdisplay.x()
    #     labelOrignY = self.originY - self.ui.label_laserdisplay.y()
    #     labelEndX = self.endX - self.ui.label_laserdisplay.x()
    #     labelEndY = self.endY - self.ui.label_laserdisplay.y()
    def PlotBloodFlow(self):
        self.plotFlag = 0
        self.plotdata = np.empty(0)
    def setLaserImage(self, p, x, y):
        #变回mat格式
        print('start set laser image')
        setLaserImage_start = datetime.datetime.now()

        yVals = y/(640*480)
        p = QPixmap.fromImage(p)
        p = p.scaled(640, 480, Qt.KeepAspectRatio)
        # # p = self.cmap2pixmap(laser,'Reds', 50)
        # # # 再转化为opencv里的图片格式，求完激光散斑再转Qimage显示
        plot_start = datetime.datetime.now()
        self.ui.label_laserdisplay.setPixmap(p)

        plot_end = datetime.datetime.now()
        print("plot cost time:", plot_end - plot_start )
        if (self.plotFlag == 1 ):
            if(self.plotdata_v1_flag):
                self.plotdata_v1 = np.append(self.plotdata_v1, y)
            # self.plotdata = np.append(self.plotdata, y)
            self.curve.setData(y)
        # self.ui.graphicsView.plotItem(y)
        # plotWidget = pg.plot(title="Three plot curves")
        # plotWidget.plot(x, yVals)
        setLaserImage_end = datetime.datetime.now()
        print('laser image display successfully and time = ', setLaserImage_end - setLaserImage_start)

    #修改截取时间
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


##激光散斑处理
    def laser_posess(self,imarray, wsize):
        posess_start = datetime.datetime.now()
        # imarray = cv2.cvtColor(imarray, cv2.COLOR_BGR2GRAY)
        # print(imarray.shape)
        print('start posess')
        imarray1 = imarray
        imarray1 = imarray.reshape(self.laserimage_height,self.laserimage_width)
        imarray1 = np.array(imarray1).astype(float)
        # print(imarray1.shape)
        # print(imarray1.dtype)  # 图像类型
        #JISUAN
        immean = ndimage.uniform_filter(imarray1, size=wsize)
        im2mean = ndimage.uniform_filter(np.square(imarray1), size=wsize)
        imcontrast = np.sqrt(abs(im2mean - np.square(immean)) / np.square(immean))
        temp = 2 * np.square(imcontrast)
        result = np.real((1 + np.sqrt(1 - temp)) / temp)
        T1 = 0.0015
        v = 1000 * ((780 * 1e-9) / (2 * np.pi * T1)) * result
        print('speckle computation finished')
        imcontrast_show = v #把（0，1）to （0，255）
        # print(np.max(imcontrast_show))
        # print(np.min(imcontrast_show))
        # print(imcontrast_show.shape)
        # print(imcontrast_show.dtype)  # 图像类型
        imcontrast_show = np.array(imcontrast_show).astype(int)
        imcontrast_show = imcontrast_show.reshape(self.laserimage_height,self.laserimage_width,1)
        # imcontrast_show = np.transpose(imcontrast_show, (1, 0, 2)).copy()

        posess_end = datetime.datetime.now()
        print('laser_posess finished and time=' , posess_end - posess_start)


        return imcontrast_show


    def changeV1Flag(self,checked):
        if checked:
            self.plotdata_v1_flag = 1
            self.plotdata_v1 = np.arange(5)
        else:
            print(self.plotdata_v1)
            file = open('log.txt', 'a')
            for fp in self.plotdata_v1:
                file.write(str(fp))
                file.write(' ')
            file.write('\n-------------------------------------我是分割线-----------------------------------------\n')
            file.close()
            self.plotdata_v1_flag = 0
            self.plotdata_v1 = np.empty(0)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())