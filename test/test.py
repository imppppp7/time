from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


# #定义坐标轴
# fig = plt.figure()
# # ax1 = plt.axes(projection='3d')
# ax2 = Axes3D(fig)
# #ax = fig.add_subplot(111,projection='3d')  #这种方法也可以画多个子图
#
# z = np.linspace(0,13,1000)
# x = 5*np.sin(z)
# y = 5*np.cos(z)
# zd = 13*np.random.random(100)
# xd = 5*np.sin(zd)
# yd = 5*np.cos(zd)
#
# ax2.scatter3D(xd,yd,zd, cmap='Blues')  #绘制散点图
# # # ax2.plot3D(x,y,z,'gray')    #绘制空间曲线
# # plt.show()

# fig = plt.figure()
# ax = Axes3D(fig)
#
# x = np.arange(0, 200)
# # print(x)
# # y = np.arange(0, 100)
# # x, y = np.meshgrid(x, y)
# z = np.random.randint(0, 200, size=(100, 200))
# print(z)
# print(z[0].shape)
#
# # y3 = np.arctan2(x, y)
# ax.scatter(x, y, z, marker='.', s=50, label='')
# plt.show()

# 抽象父类： 父类提供整个框架，子类来完成各种工作


class Person:
    def miss(self):
        self.anta()

    def anta(self):
        assert False, 'anta must be defined!'


class Man(Person):
    def anta(self):
        print('hello world')


x = Man()
x.miss()