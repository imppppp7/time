
import numpy as np
from laserspeckle_process import mvsdk
from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import PyQt5.QtGui as  Qtgui
import time
import datetime

class Thread(QThread):
    #图片改变信号
    changePixmap = pyqtSignal(QImage)
    laser_posess = pyqtSignal(QImage)
    #相机初始参数设定
    isCapture = 0
    isCameraSettingChanged = 0
    Exposuretime = 60
    Gain = 0
    #10帧传递一张处理
    fps_flag=0
    fps_interval=2

    fps_sum = 0
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
        mvsdk.CameraSetExposureTime(hCamera, self.Exposuretime * 1000)

        # 让SDK内部取图线程开始工作
        mvsdk.CameraPlay(hCamera)
        # print(mvsdk.CameraCustomizeResolution(hCamera))
        #
        mvsdk.CameraSetImageResolution(hCamera,mvsdk.CameraCustomizeResolution(hCamera))
        print(mvsdk.CameraGetImageResolution(hCamera))
        print("set camera finished ")
        # 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
        FrameBufferSize = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax * (1 if monoCamera else 3)
        # FrameBufferSize = 640 *480
        # 分配RGB buffer，用来存放ISP输出的图像
        # 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据（如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer）
        pFrameBuffer = mvsdk.CameraAlignMalloc(FrameBufferSize, 16)
        capture_all_start = datetime.datetime.now()
        print('camera init finished')
        while True:

                capture_start = datetime.datetime.now()

                pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
                flag_start1 = datetime.datetime.now()
                mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
                flag_start2 = datetime.datetime.now()
                mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)
                flag_start3 = datetime.datetime.now()
                # 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
                # 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
                frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)
                print("flag1 cost time :", flag_start1-capture_start)
                print("flag2 cost time :", flag_start2-flag_start1)
                print("flag3 cost time :", flag_start3-flag_start2)
                frame = np.frombuffer(frame_data, dtype=np.uint8)
                frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth,
                                       1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3))
                capture_end = datetime.datetime.now()
                self.fps_sum+=1
                print('截取{0}张图,本次截取所用时间{1},总时间为{2}'.format(self.fps_sum, capture_end-capture_start,capture_end-capture_all_start))
                print('{0} and {1}'.format('spam', 'eggs'))
                #将图片转为QT格式的
                print('rawimage size',frame.shape)
                rawImage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                #图片旋转

                trans = Qtgui.QTransform()
                trans.rotate(180)
                rawImage = rawImage.transformed(
                     trans, Qt.SmoothTransformation)
                # 显示图片
                self.changePixmap.emit(rawImage)
                self.fps_flag=self.fps_flag+1

                #12/26 18:36
                if self.fps_flag>self.fps_interval:
                    #传递图片给激光散斑处理
                    self.laser_posess.emit(rawImage)
                    print("sent laser_raw_image")
                    self.fps_flag=0

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
                    status = mvsdk.CameraSaveImage(hCamera, "D:\\" + PictureName + ".bmp", pFrameBuffer, FrameHead,
                                                   mvsdk.FILE_BMP_8BIT if monoCamera else mvsdk.FILE_BMP, 100)
                    print("capturePicture")

                    if status == mvsdk.CAMERA_STATUS_SUCCESS:
                        print("Save image successfully. image_size = {}X{}".format(FrameHead.iWidth,
                                                                                   FrameHead.iHeight))
                    else:
                        print("Save image failed. err={}".format(status))
                time.sleep(0.01)
                self.isCapture = 0
    #采集图片flag
    def capturePicture(self):
        print ("capture")
        self.isCapture=1
    #相机设置改变flag
    def CameraSettingChanged(self):
        print ("CameraSettingChanged")
        self.isCameraSettingChanged = 1
    #相机曝光时间更改flag
    def CameraSettingExposuretime(self,value):
        self.Exposuretime = value
    #相机增益改变flag
    def CameraSettingGain(self,value):
        self.Gain = value