import sys
import numpy as np
import mvsdk
import cv2
from PyQt5.QtWidgets import QApplication, QLabel ,QWidget, QDialog
from camera import Ui_widget
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
import datetime

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    #相机初始参数设定
    isCapture = 0
    isCameraSettingChanged = 0
    Exposuretime = 30
    Gain = 16

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)


    def run(self):

        #相机的获取与运行
        DevList = mvsdk.CameraEnumerateDevice()
        nDev = len(DevList)
        if nDev < 1:
            print("No camera was found!")
            return

        DevInfo = DevList[0]
        print(DevInfo)

        # 打开相机
        hCamera = 0
        try:
            hCamera = mvsdk.CameraInit(DevInfo, -1, -1)
        except mvsdk.CameraException as e:
            print("CameraInit Failed({}): {}".format(e.error_code, e.message))
            return

        # 获取相机特性描述
        cap = mvsdk.CameraGetCapability(hCamera)

        # 判断是黑白相机还是彩色相机
        monoCamera = (cap.sIspCapacity.bMonoSensor != 0)

        # 黑白相机让ISP直接输出MONO数据，而不是扩展成R=G=B的24位灰度
        if monoCamera:
            mvsdk.CameraSetIspOutFormat(hCamera, mvsdk.CAMERA_MEDIA_TYPE_MONO8)

        # 相机模式切换成连续采集
        mvsdk.CameraSetTriggerMode(hCamera, 0)

        # 手动曝光，曝光时间30ms
        mvsdk.CameraSetAeState(hCamera, 0)
        mvsdk.CameraSetExposureTime(hCamera, 30 * 1000)

        # 让SDK内部取图线程开始工作
        mvsdk.CameraPlay(hCamera)

        # 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
        FrameBufferSize = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax * (1 if monoCamera else 3)

        # 分配RGB buffer，用来存放ISP输出的图像
        # 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据（如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer）
        pFrameBuffer = mvsdk.CameraAlignMalloc(FrameBufferSize, 16)
        while True:

                pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
                mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
                mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)

                # 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
                # 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
                frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)

                frame = np.frombuffer(frame_data, dtype=np.uint8)
                frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth,
                                       1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3))
                #将图片转为QT格式的
                rawImage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_Indexed8)
                self.changePixmap.emit(rawImage) #显示图片
                #是否相机设置发生更改
                if self.isCameraSettingChanged:
                    print("CameraSettingChanged")
                    #修改曝光时间
                    print("修改后的曝光时间",self.Exposuretime)
                    mvsdk.CameraSetExposureTime(hCamera, self.Exposuretime * 1000)
                    #修改FPS

                    #修改增益
                    print("修改后的增益", self.Gain)
                    mvsdk.CameraSetAnalogGain(hCamera, self.Gain)

                    #修改完毕
                    self.isCameraSettingChanged=0
                #是否截图 单张截图
                if self.isCapture:
                    print("capturePicture")
                    #获取当前时间作为图片名称
                    PictureName = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    print(PictureName)
                    status = mvsdk.CameraSaveImage(hCamera, "D:\\"+PictureName+".bmp", pFrameBuffer, FrameHead,
                                                   mvsdk.FILE_BMP_8BIT if monoCamera else mvsdk.FILE_BMP, 100)
                    print("capturePicture")

                    if status == mvsdk.CAMERA_STATUS_SUCCESS:
                        print("Save image successfully. image_size = {}X{}".format(FrameHead.iWidth,
                                                                                   FrameHead.iHeight))
                    else:
                        print("Save image failed. err={}".format(status))
                self.isCapture = 0

    def capturePicture(self):
        print ("capture")
        self.isCapture=1
    def CameraSettingChanged(self):
        print ("CameraSettingChanged")
        self.isCameraSettingChanged = 1
    def CameraSettingExposuretime(self,value):
        self.Exposuretime = value
    def CameraSettingGain(self,value):
        self.Gain = value




class App(QWidget):
    #几个传递值的信号
    ExposuretimeChangedValue = pyqtSignal(int )
    GainChangedValue = pyqtSignal(int)

    def __init__(self):
            super(App,self).__init__()
            self.ui = Ui_widget()
            self.ui.setupUi(self)
            self.title = 'PyQt4 Video'

            self.initUI()

    def initUI(self):
            # self.setWindowTitle(self.title
            # self.setGeometry(self.left, self.top, self.width, self.height)
            # self.resize(800, 600)
            # # create a label
            # self.label = QLabel(self)
            # self.label.move(0, 0)
            # self.label.resize(640, 480)

            th = Thread(self)
            th.changePixmap.connect(lambda p: self.setPixMap(p))  # 将changePixmap 函数与setPixMap 函数 联系起来
            self.ui.label_CaptureFrame.clicked.connect(th.capturePicture)
            self.ui.horizontalSlider_SetExposure.valueChanged.connect(self.on_changed_ExposureTime)
            self.ui.horizontalSlider_SetExposure.valueChanged.connect(th.CameraSettingChanged)
            self.ui.horizontalSlider_Setfps.valueChanged.connect(th.CameraSettingChanged)
            self.ui.horizontalSlider_SetGain.valueChanged.connect(th.CameraSettingChanged)
            self.ui.horizontalSlider_SetGain.valueChanged.connect(self.on_changed_Gain)
            self.ExposuretimeChangedValue.connect(lambda value: th.CameraSettingExposuretime(value))
            self.GainChangedValue.connect(lambda value: th.CameraSettingExposuretime(value))
            #还差保持路径、截取间隔、还有截取时间
            th.start()


    def on_changed_ExposureTime(self, value):
        Exposuretime = self.ui.horizontalSlider_SetExposure.value()
        print(Exposuretime)
        self.ExposuretimeChangedValue.emit(Exposuretime)

    def on_changed_Gain(self, value):
        Gain = self.ui.horizontalSlider_SetGain.value()
        print(Gain)

        self.GainChangedValue.emit(Gain)
    def setPixMap(self, p):
        p = QPixmap.fromImage(p)
        p = p.scaled(640, 480, Qt.KeepAspectRatio)
        self.ui.label_VideoDisplay.setPixmap(p)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())