from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtGui import QImage
import PyQt5.QtGui as  Qtgui

class LaserThread(QThread):
    # 激光散斑图片改变信号
    change_laser = pyqtSignal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)

    def run(self):
        #获取图片
        for i in range(20030):
            pass

        #图片激光散斑处理
        self.Laser_posess();


    def Laser_posess(self,image):
        print(111)
    def show_raw_img(self, p):
        img = p
        print("show_raw_img")
        self.change_laser.emit(p)