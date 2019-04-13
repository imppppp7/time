# coding=utf-8
import cv2
import numpy as np
import mvsdk
import datetime


def main_loop():
    # 枚举相机
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

    # 相机模式切换成软触发采集
    mvsdk.CameraSetTriggerMode(hCamera, 1)

    # 获取相机的触发模式
    mvsdk.CameraGetTriggerMode(hCamera)

    # 设置闪光灯STROBE信号的模式 0是自动，不能设置延迟时间，和脉冲宽度，1是手动
    mvsdk.CameraSetStrobeMode(hCamera, 0)
    mvsdk.CameraGetstrobeMode(hCamera)

    # 设置高低电平模式
    mvsdk.CameraSetStrobePolarity(hCamera, 1)
    mvsdk.CameraGetStrobePolarity(hCamera)

    # # 设置延迟时间
    mvsdk.CameraSetStrobeDelayTime(hCamera, 0)
    #
    # # 设置脉冲宽度,单位是微秒 和相机曝光时间相等
    # mvsdk.CameraSetStrobePulseWidth(hCamera, 1000)

    # 手动曝光，设置曝光时间,(exposureTime的单位是微秒)
    mvsdk.CameraSetAeState(hCamera, 0)
    mvsdk.CameraSetExposureTime(hCamera, 1 * 1000)
    mvsdk.CameraGetExposureTime(hCamera)

    # 设置增益，获得增益
    mvsdk.CameraSetAnalogGain(hCamera, 2)
    mvsdk.CameraGetAnalogGain(hCamera)

    # 设置相机的帧率,并返回帧率大小
    mvsdk.CameraSetFrameSpeed(hCamera, 1)
    mvsdk.CameraGetFrameSpeed(hCamera)

    # 让SDK内部取图线程开始工作
    mvsdk.CameraPlay(hCamera)

    # 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
    FrameBufferSize = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax * (1 if monoCamera else 3)

    # 分配RGB buffer，用来存放ISP输出的图像
    # 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据（如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer）
    pFrameBuffer = mvsdk.CameraAlignMalloc(FrameBufferSize, 16)

    while (cv2.waitKey(1) & 0xFF) != ord('q'):
        # 从相机取一帧图片
        try:
            start = datetime.datetime.now()
            print('每一帧花费的时间',start)
            mvsdk.CameraSoftTrigger(hCamera)
            pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
            mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
            mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)

            # 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
            # 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
            frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)
            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth,
                                   1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3))

            cv2.imshow("capture", frame)

        except mvsdk.CameraException as e:
            if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
                print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message))

    # 关闭相机
    mvsdk.CameraUnInit(hCamera)

    # 释放帧缓存
    mvsdk.CameraAlignFree(pFrameBuffer)


def main():
    try:
        main_loop()
    finally:
        cv2.destroyAllWindows()


main()


