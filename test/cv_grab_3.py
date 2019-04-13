#coding=utf-8
# from model_set import create_espon
#中文无法显示
#coding=utf-8
import cv2
import mvsdk
# from model_set import create_espon
from PIL import Image
import test
import screeninfo
#中文无法显示
from pylab import *

mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False
# fx=0.6
# fy=0.6
# l=50
# t=50

##常见错误：霍夫圆检测不到——1 canny算子的参数 2 相机的曝光和增益
##颜色矫正出问题——色块的检测不准——1 检测起点步长  2 ROI长度

# ######################################这里是深度学习代码的转换
# class deep_convert:
# 	def __init__(self,input_image):
# 		#输入图片
# 		self.deep_c(input_image)
# 	#读取cv格式的图，brg
# 	def deep_c(self,img):
# 		# 保存到keras格式中
# 		w,h,d=img.shape
# 		Y=np.empty((1,3,w,h),dtype='float32')
# 		Y[0,:,:,:]=[img[:,:,2],img[:,:,1],img[:,:,0]]
# 		#归一化
# 		Y=Y.astype('float')/255
# 		Y=np.transpose(Y,[0,2,3,1])
# 		model=create_espon()
# 		pre=model.predict(Y,batch_size=1)*255
# 		pre=pre.astype(np.uint8)
# 		pre=np.transpose(pre,[0,3,1,2])
# 		r=Image.fromarray(pre[0]).convert('L')
# 		g=Image.fromarray(pre[1]).convert('L')
# 		r=Image.fromarray(pre[0]).convert('L')
# 		image=Image.merge('RGB',(r,g,b))
# 		return image


#####################################这里是矩阵计算的思路转化

#投影仪初始
#投影设置 参考 https://www.cnblogs.com/xlqtlhx/p/8117820.html
#添加投影框
img_0=np.zeros([800,1280,3],np.uint8)
# img_0[:,:,:][145:800][:,195:205]=255
# img_0[:,:,:][135:145][:,195:1073]=255
# img_0[:,:,:][135:800][:,1063:1073]=255
# img_0[:,:,:][790:800][:,195:1073 ]=255

img2 = np.zeros([800, 1280, 3], np.uint8)
# img2[:,:,:][145:800][:,195:205]=255
# img2[:,:,:][135:145][:,195:1073]=255
# img2[:,:,:][135:800][:,1063:1073]=255
# img_0[:,:,:][790:800][:,195:1073 ]=255
# img2 = np.zeros((1024, 1920, 3), np.uint8)


# cv2.imshow('1',img_0)
# cv2.waitKey()
def projector_(id):
	screen_id=id
	# is_color=False#是彩图还是单值图
	# #显示器信息
	# for n in screeninfo.get_monitors():
	# 	print(str(n))
	# get the size of the screen
	screen=screeninfo.get_monitors()[screen_id]
	#这里的为扩展，所以第二个屏幕的起点为（1920，0）
	# print('x,y',screen.x,screen.y)
	width,height=screen.width,screen.height #id屏幕的分辨率
	# print('w,d',width,height)

	# # create image
	# if is_color:
 	#     image[:10, :10] = 0  # black at top-left corner
	#     image[height - 10:, :10] = [1, 0, 0]  # blue at bottom-left
	#     image[:10, width - 10:] = [0, 1, 0]  # green at top-right
	#     image[height - 10:, width - 10:] = [0, 0, 1]  # red at bottom-right
	# else:

	#     image = np.ones((height, width), dtype=np.float32)
	#     image[0, 0] = 0  # top-left corner
	#     image[height - 2, 0] = 0  # bottom-left
	#     image[0, width - 2] = 0  # top-right
	#     image[height - 2, width - 2] = 0  # bottom-right


	# #背景图
	# #TODO 包括全图800*1280
	# img=np.ones([800,1280,3],np.uint8)
	# img=img[:,:,:][20:780][:,20:1260]
	# # cv2.imshow('res',img)
	# # cv2.waitKey()
	# #自己读图
	# I = cv2.imread(r'E:\pycharm\camera\test.bmp')
	# # print('I',I.shape)
	# #这个比例要矫正 #TODO
	# I=cv2.resize(I,None,fx=0.75,fy=0.75)
	# w,h,d=I.shape
	# # cv2.imshow('img',I)
	# # cv2.waitKey()
	# #TODO :依据图像设参数
	# 将相机的图像贴图到背景中
	# #起点 l,t
	# l,t=0,0
	# img[l:l+w,t:t+h,0]=I[:,:,0]
	# img[l:l+w,t:t+h,1]=I[:,:,1]
	# img[l:l+w,t:t+h,2]=I[:,:,2]

	#全屏显示的
	cv2.namedWindow('projector%d'% (id), cv2.WINDOW_AUTOSIZE)
	cv2.moveWindow('projector%d'% (id), screen.x, screen.y-100)
	# cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
	# 					  cv2.WINDOW_FULLSCREEN)
	if id==0:
	   cv2.imshow('projector%d'% (id), img_0)
	else:
	   cv2.imshow('projector%d' % (id), img2)
	# cv2.waitKey()
	# cv2.destroyAllWindows()

	# cv2.namedWindow('projector',cv2.WINDOW_AUTOSIZE)#constrain the size by the displayed image. the window is not resizable
	#通过设置上面的后面的一个参数应该不用下面的调整了，先隐藏
	# #设置窗口大小，使得投影的图片大小与相机采集的图片大小一致
	# cv2.resizeWindow(window_name,w,h)
	#还是需要图片的长宽 w,h
	# w,h=480,854
	#可能需要计算比例
	# print(screen.x+int(width/2-w/2),screen.y+int(height/2-h/2))
	# cv2.moveWindow(window_name,screen.x+100,screen.y+100)
	# cv2.setWindowProperty(window_name,cv2.WND_PROP_AUTOSIZE,cv2.WINDOW_AUTOSIZE)
	# cv2.imshow(window_name,I)
	# cv2.waitKey()
	# cv2.destroyAllWindows()
projector_(0)
# cv2.imshow('projector%d'% (id), img_0)
projector_(1)

cv2.waitKey(0)

#利用霍夫圆检测获取中心
#https://blog.csdn.net/haofan_/article/details/77625843

####这里有时检测不到圆时，可以调节canny的参数或者相机的增益

def circle_detect(I):
	#BGR图片
	#将BGR图灰度化
	gray=cv2.cvtColor(I,cv2.COLOR_BGR2GRAY)
	canny=cv2.Canny(gray,30,60)#左边是minval，右边是maxval，低于minval舍弃，图像灰度梯度 高于maxVal被认为是真正的边界，低于minVal的舍弃。
								# 两者之间的值要判断是否与真正的边界相连，相连就保留，不相连舍弃
	#canny = cv2.Canny(gray, 30, 60)
	#显示canny算子分割结果
	cv2.namedWindow('canny',cv2.WINDOW_NORMAL)
	cv2.imshow('canny',canny)
	cv2.waitKey()
	#输出图片的尺寸
	print('circle_pic_shape',I. shape)
	#霍夫检测圆
	circles = cv2.HoughCircles(canny, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=30, minRadius=10, maxRadius=100)
	#输出返回值
	print('circle信息',circles[0])

	#检测圆的个数
	print('1111',len(circles[0]),)
	assert 4==len(circles[0]),'检测圆的个数不匹配4，可以调节canny的参数或者相机的增益'
	#画图看看显示检测结果
	# 记录4个点
	point = [[0, 0], [0, 0], [0, 0], [0, 0]]
	#起点
	x_m,y_m=np.mean(circles[0],axis=0)[0],np.mean(circles[0],axis=0)[1]
	for circle in circles[0]:
		# 坐标行列
		x = int(circle[0])#横着的
		y = int(circle[1])#竖着的
		# #起点小于均值搞的
		if (x<=x_m and y<=y_m):
			point[0][0]=x
			point[0][1]=y
		elif (x>=x_m and y<=y_m):
			point[1][0]=x
			point[1][1]=y
		elif (x <= x_m and y >= y_m):
			point[2][0] = x
			point[2][1] = y
		else:
			point[3][0] = x
			point[3][1] = y
		# 半径
		r = int(circle[2])
		# 在原图用指定颜色标记出圆的位置
		# I = cv2.circle(I, (x, y), r, (0, 0, 255), -1)

	#显示检测到的4点坐标（1轴，0轴）
	print('检测坐标',point)
	# #显示霍夫结果
	# cv2.namedWindow('ori_hufu_circle',cv2.WINDOW_NORMAL)
	# cv2.imshow('ori_hufu_circle',I)
	# cv2.waitKey(0)
	h,w=I.shape[:2]
	#新加仿射变换
	src = np.array(point, np.float32)
	#这里需要一个标准图来矫正提前获得这几个标准位置
	dst = np.array([[163,118 ], [1118, 118], [163, 850], [1118, 850]], np.float32)
	#变换矩阵
	P = cv2.getPerspectiveTransform(src, dst)
	#变换
	I = cv2.warpPerspective(I, P, (w, h), borderValue=(255,255,255))  # 先1后0
	cv2.namedWindow('warpp',cv2.WINDOW_NORMAL)
	cv2.imshow('warpp',I)
	#按任意键退出
	cv2.waitKey(0)
	res=[[160,120 ], [1120, 120], [160, 850], [1120, 850]]
	print('返回坐标',res)
	# cv2.waitKey(0)
	return res,I
#验证霍夫检测
# img=cv2.imread(r'E:\pycharm\camera\navigationWithZ\camera_develop\img_correction\ori_tiqu.png')
# img=cv2.imread(r'E:\pycharm\camera\navigationWithZ\camera_develop\result\color_correct\x.bmp')
# img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
# circle_detect(img)

# 矩阵dot运算
#获取矫正矩阵
#全局变量
#事前获得的一个矫正矩阵

T = np.array([[1.11474406852460,	-0.416239649493069,	0.0587588863048835,	-0.206305216650330,	-2.37751838104525,	-0.312520267834230,	1.11181839672126,	-0.247283090250991,	1.61163682479560,	7.27559804733092e-05],
			[-0.554881808715815,	4.70108383774244,	-0.401708544538281,	1.15106712534459,	16.5608632882958,	1.88470414723525,	-7.10730515758390,	1.66372918801411,	-10.8074249834294,	-0.000301396854660002],
			[0.187819416218754,	-1.24840423958439,	1.22477446607366,	-0.426992597453845,	-5.64597971211758,	-0.628384738726316,	2.92242684355067,	-0.741136953109371,	3.59264706607614,	0.000174244215876242]],dtype=np.double)

#矫正失败跟这个ROI选取还是有很大关系的，所以矫正要尽可能的放正
def correct_m(X,Y,x,y):
	'''

	:param X: 正常图，要归一化输入
	:param Y: 失通道图，要归一化输入
	:param x: 起点 4点坐标（1，0）
	:param y: 起点  4点坐标
	:param step: ROI步长
	:param length_ROI: ROI长宽
	:return: 矫正矩阵T
	'''
	# w_X,h_X,d_X=X.shape
	# w_Y,h_Y,d_Y=Y.shape
	# # print(X.shape)
	# assert w_X==w_Y and h_X==h_Y and d_X==d_Y , '图片不匹配'
	#保存rgb的点像素值
	n=108
	# print('n',n)
	#org
	r_org=np.zeros((n,1))
	g_org=np.zeros((n,1))
	b_org=np.zeros((n,1))
	#flt
	r_flt=np.zeros((n,1))
	g_flt=np.zeros((n,1))
	b_flt=np.zeros((n,1))
	#index
	k=0
	length_ROI=20
	#步长，纵向
	s0=(x[-1][1]-x[0][1])//8
	s1=(x[-1][0]-x[0][0])//11
	#选择ROI,并计算均值赋值给上面矩阵
	# print(x)
	for i in range(x[0][1],x[-1][1],s0):#纵向
		for j in range(x[0][0],x[-1][0],s1):#横向
			# 选取ROI
			# print(i,j)
			# img = cv2.circle(X, (j, i), 5, (0, 0, 255), -1)
			# cv2.imshow('imggg',img)
			# cv2.imshow('失通道每个方块im',X[:, :, :][i-length_ROI:i + length_ROI][:, j-length_ROI:j + length_ROI])
			# cv2.waitKey(0)
			# 正常图
			r_org[k] = np.mean(X[:, :, 0][i-length_ROI:i + length_ROI][:, j-length_ROI:j + length_ROI])
			g_org[k] = np.mean(X[:, :, 1][i-length_ROI:i + length_ROI][:, j-length_ROI:j + length_ROI])
			b_org[k] = np.mean(X[:, :, 2][i-length_ROI:i + length_ROI][:, j-length_ROI:j + length_ROI])
			k+=1
	k=0
	for i in range(y[0][1],y[-1][1],s0):#纵向
		for j in range(y[0][0],y[-1][0],s1):#横向
			# 选取ROI
			#显示每个方块
			# img = cv2.circle(Y, (j, i), 5, (0, 0, 255), -1)
			# cv2.imshow('imggg',img)
			# cv2.imshow('失通道每个方块im',Y[:, :, :][i:i + length_ROI][:, j:j + length_ROI])
			# cv2.waitKey(0)
			# 失通道图
			r_flt[k] = np.mean(Y[:, :, 0][i:i + length_ROI][:, j:j + length_ROI])
			g_flt[k] = np.mean(Y[:, :, 1][i:i + length_ROI][:, j:j + length_ROI])
			b_flt[k] = np.mean(Y[:, :, 2][i:i + length_ROI][:, j:j + length_ROI])
			k+=1

	#计算矫正矩阵
	one=np.ones((n,1))
	#中间矩阵

	A=np.concatenate((r_flt,g_flt,b_flt,r_flt*r_flt,g_flt*g_flt,b_flt*b_flt,r_flt*g_flt,r_flt*b_flt,g_flt*b_flt,one),axis=1)
	a1=np.dot(np.dot(np.linalg.inv(np.dot(A.T,A)),A.T),r_org)
	a2=np.dot(np.dot(np.linalg.inv(np.dot(A.T,A)),A.T),g_org)
	a3=np.dot(np.dot(np.linalg.inv(np.dot(A.T,A)),A.T),b_org)
	T=np.concatenate((a1.T,a2.T,a3.T),axis=0)
	print(T)
	return T

# #先以手动输入图
# X=cv2.imread(r'E:\pycharm\camera\navigationWithZ\camera_develop\feature_s_m\n2.png')
# X=cv2.cvtColor(X,cv2.COLOR_BGR2RGB)
# Y=cv2.imread(r'E:\pycharm\camera\navigationWithZ\camera_develop\feature_s_m\n2.png')
# Y=cv2.cvtColor(Y,cv2.COLOR_BGR2RGB)
# x=circle_detect(X)
# y=circle_detect(Y)
# T=correct_m(X/255.0, Y/255.0, x, y)

#相机获取矫正图片
def camera():
	# 枚举相机
	img=0
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
	mvsdk.CameraSetExposureTime(hCamera, 40 * 1000)

	# # #手动增益

	mvsdk.CameraSetGain(hCamera,200,200,200)
	print(mvsdk.CameraGetGain(hCamera))

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
			pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
			mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
			mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)

			# 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
			# 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
			frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)
			frame = np.frombuffer(frame_data, dtype=np.uint8)
			frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth, 1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3))#numpy格式的图片
			# #旋转
			w,h=frame.shape[:2]
			# print(w,h)
			M=cv2.getRotationMatrix2D((h/2,w/2),180,1)
			frame_=cv2.warpAffine(frame,M,(h,w))
			#翻转
			# frame=cv2.flip(frame,1)
			cv2.namedWindow('correct_capture',cv2.WINDOW_NORMAL)
			cv2.imshow("correct_capture", frame_)
			#返回结果
			c=cv2.waitKey(1)
			if c == 32:
				img = frame_
				break
		except mvsdk.CameraException as e:
			if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
				print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message))

	# 关闭相机
	mvsdk.CameraUnInit(hCamera)

	# 释放帧缓存
	mvsdk.CameraAlignFree(pFrameBuffer)

	#关闭窗口
	cv2.destroyWindow('correct_capture')
	return img
#相机
camera()
#矫正
def correct():
	#BGR对BGR的矫正
	print('正常图，并按space保存')
	X=camera()
	cv2.imwrite(r'E:\pycharm\camera\navigationWithZ\camera_develop\result\color_correct\x.bmp',X)
	cv2.imshow('ori1',X)
	cv2.waitKey()
	print('失通道图,并按space保存')
	Y=camera()
	cv2.imwrite(r'E:\pycharm\camera\navigationWithZ\camera_develop\result\color_correct\y.bmp',Y)
	cv2.imshow('flt',Y)
	cv2.waitKey()
	X=cv2.cvtColor(X,cv2.COLOR_BGR2RGB)
	Y = cv2.cvtColor(Y, cv2.COLOR_BGR2RGB)
	plt.figure()
	plt.subplot(121)
	plt.imshow(X)
	plt.title('org')
	plt.subplot(122)
	plt.imshow(Y)
	plt.title('flt')
	plt.show()
	#计算起点
	X=cv2.cvtColor(X,cv2.COLOR_RGB2BGR)
	Y = cv2.cvtColor(Y, cv2.COLOR_RGB2BGR)
	#滤波
	X=cv2.GaussianBlur(X,(0,0),1.8)
	Y=cv2.GaussianBlur(Y,(0,0),1.8)
	# X=cv2.blur(X,(5,5))
	# Y=cv2.blur(Y,(5,5))
	X=cv2.medianBlur(X,5)
	Y=cv2.medianBlur(Y,5)
	#提取变换
	x,X=circle_detect(X)
	y,Y=circle_detect(Y)
	#显示输入结果
	# #验证好了后，进行矫正
	# cv2.imshow('输入x',X)
	# cv2.waitKey(0)
	# cv2.imshow('输入y',Y)
	# cv2.waitKey(0)

	# #处理用
	# X_=X[74:890,120:1162]
	# Y_ = Y[74:890, 120:1162]
	# print('shape',X_.shape,Y_.shape)
	# cv2.imwrite(r'E:\pycharm\camera\navigationWithZ\camera_develop\result\capture\ori.bmp',X_)
	# cv2.imwrite(r'E:\pycharm\camera\navigationWithZ\camera_develop\test_pic\flt1_crop.bmp',Y_)
	# 归一化输入
	global T
	T=correct_m(X/255.0,Y/255.0,x,y)

#correct 验证
# correct()
# print('T',T)
#上面目前没问题



# #点计算
# def array_pix_dot(r,g,b):
# 	#单像素点输入
# 	# 创建中间矩阵 10*1
# 	new_array=np.array([r,g,b,r**2,g**2,b**2,r*g,r*b,g*b,1],dtype=np.double)[:,np.newaxis]
# 	# 查看中间矩阵
# 	# print('new-array', new_array,type(new_array),new_array.shape)
# 	#返回dot矩阵
# 	global T
# 	res=np.dot(T,new_array)
# 	# print('dot',res,res.shape)
# 	return res
# def image_pix_input(I):
# 	t0 = time.time()
# 	w, h, d = I.shape
# 	# 归一化
# 	I = I / 255.0
# 	#单像素点
# 	#结果
# 	res=np.zeros((w,h,d))
# 	for i in range(w):
# 		for j in range(h):
# 			#提取每个像素点
# 			temp=I[i,j,:]
# 			# #检验
# 			# print(temp)
# 	# 		# cv2.waitKey()
# 			#像素dot后的结果
# 			pix_dot=array_pix_dot(temp[0],temp[1],temp[2])
# 			# print(pix_dot)
# 			#处理越界问题
# 			pix_dot[0]=pix_dot[0]*255
# 			pix_dot[1]=pix_dot[1]*255
# 			pix_dot[2]=pix_dot[2]*255
# 			if pix_dot[0]<0:
# 				pix_dot[0]=0
# 			elif pix_dot[0]>255:
# 				pix_dot[0]=255
# 			if pix_dot[1]<0:
# 				pix_dot[1]=0
# 			elif pix_dot[1]>255:
# 				pix_dot[1]=255
# 			if pix_dot[2]<0:
# 				pix_dot[2]=0
# 			elif pix_dot[2]>255:
# 				pix_dot[2]=255
# 			# res[i,j,:]=[pix_dot[2],pix_dot[1],pix_dot[0]]
# 			res[i,j,:]=[pix_dot[0],pix_dot[1],pix_dot[2]]
# 	#转成图片
# 	# print('res',res.shape,type(res))
# 	res=Image.fromarray(res.astype(np.uint8))
#
# 	# 验证
# 	# print(type(res))
# 	# print(res,res.shape)
# 	# 显示
# 	# #PIL格式显示
# 	# plt.imshow(res)
# 	# plt.show()
# 	# PIL与opencv的转换 :https://blog.csdn.net/dcrmg/article/details/78147219
# 	res=cv2.cvtColor(np.asarray(res),cv2.COLOR_RGB2BGR)
# 	# cv显示验证
# 	cv2.imshow('image',res)
# 	t1 = time.time()
# 	print(t1 - t0)
# 	# cv2.waitKey()
# 	return res

#矩阵计算
def  array_dot(r,g,b,w,h):
	#将r,g,b分别当矩阵，分别是对应的单通道,现在是以bgr输入为rgb的
	#矩阵构建中间矩阵
	one_d=np.ones((w,h))
	new_array_m=np.array([r,g,b,r*r,g*g,b*b,r*g,r*b,g*b,one_d],dtype=np.double)[:,np.newaxis] #结果是10*1*w*h
	new_array_m=np.transpose(new_array_m,[2,3,0,1]) #转化为可矩阵计算的尺寸
	#计算dot运算
	global T
	res=np.dot(T,new_array_m)
	# print(res.shape)
	res=np.transpose(res,[3,1,2,0])*255
	# print(res,res.shape)
	# cv2.waitKey()
	#返回的是BGR
	return res[0]

def image_input(I):
	'''

	:param I: 不用归一化的，BGR
	:return:
	'''
	t0= test.time()
	#归一化
	I=cv2.pyrDown(I)
	I=I/255.0
	w, h, d = I.shape
	#矩阵矫正
	img_dot=array_dot(I[:,:,0],I[:,:,1],I[:,:,2],w,h)
	# print(type(img_dot),img_dot.shape)

	img_dot[img_dot>255]=255
	img_dot[img_dot<0]=0

	res=Image.fromarray(img_dot.astype(np.uint8))
	res=np.asarray(res)
	#验证
	# print(type(res))
	# print(res,res.shape)
	#显示
	# #PIL格式显示
	# plt.imshow(res)
	# plt.show()
	#PIL与opencv的转换 :https://blog.csdn.net/dcrmg/article/details/78147219
	# res=cv2.cvtColor(np.asarray(res),cv2.COLOR_RGB2BGR)
	# #视频显示
	# (r,g,b)=cv2.split(res)
	# res=cv2.merge([b,g,r])
	# res=cv2.cvtColor(np.asarray(res),cv2.COLOR_RGB2RGBA)
	#cv显示验证
	# cv2.imshow('image_jiaozhen',res)
	# cv2.waitKey()
	t1= test.time()
	print('每帧时间：',t1-t0)
	res=cv2.pyrUp(res)
	# #单张图使用
	# res = cv2.GaussianBlur(res, (0,0),1.8)
	# res = cv2.medianBlur(res, 5)
	# cv2.namedWindow('image_',cv2.WINDOW_NORMAL)
	# cv2.imshow('image_', res)
	# #保存
	# cv2.imwrite(r'E:\pycharm\camera\navigationWithZ\camera_develop\result\capture\correct.bmp', res)
	return res

# #先用一张图实验看看
# #读图
# I=cv2.imread(r'E:\pycharm\camera\navigationWithZ\camera_develop\test_pic\flt2.BMP')
# # I=cv2.blur(I,(5,5))
# # I=cv2.medianBlur(I,5)
# #将读进来的bgr-rgb
# # I=cv2.cvtColor(I,cv2.COLOR_BGR2RGB)
# # #显示
# # cv2.imshow('image',I)
# # cv2.waitKey()
# # print(I,I.shape,type(I))
# #矩阵
# image_input(I)
# #点
# # image_pix_input(I)
# cv2.waitKey()
# mouse callback function

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = 1,1




        # if mode == True:
        #     cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        # else:
        #     img[y - 5:y + 5, x - 5:x + 5, :] = img_copy[y - 5:y + 5, x - 5:x + 5, :]
img_3 = np.zeros([800,1280,3],np.uint8)
def draw_circle(event,x,y,flags,param):

    global ix, iy, drawing, mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv2.circle(img_3, (x, y), 4, (0, 255, 0), -1)
            # else:
            #     img_0[y - 25:y + 25, x - 25:x + 25, :] = img_copy[y - 25:y + 25, x - 25:x + 25, :]
            #     img2[y - 25:y + 25, x - 25:x + 25, :] = img2_copy[y - 25:y + 25, x - 25:x + 25, :]
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
                # else:
                #     img2[y2 - 25:y2 + 25, x2 - 25:x2 + 25, :] = img2_copy[y2 - 25:y2 + 25, x2 - 25:x2 + 25, :]

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False


cv2.setMouseCallback('projector0', draw_circle)
cv2.setMouseCallback('projector1', copy_circle)

def main_loop():
	l=50
	t=50
	fx = 0.4
	fy = 0.4
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
		print("CameraInit Failed({}): {}".format(e.error_code, e.message) )
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

	# 手动曝光，曝光时间40ms
	mvsdk.CameraSetAeState(hCamera, 0)
	mvsdk.CameraSetExposureTime(hCamera, 30 * 1000)

	# # #手动增益
	# print('相机增益', mvsdk.CameraGetGain(hCamera))
	# #RGB的每个通道增益
	mvsdk.CameraSetGain(hCamera,200,200,200)

	# 让SDK内部取图线程开始工作
	mvsdk.CameraPlay(hCamera)

	# 计算RGB buffer所需的大小，这里直接按照相机的最大分辨率来分配
	FrameBufferSize = cap.sResolutionRange.iWidthMax * cap.sResolutionRange.iHeightMax * (1 if monoCamera else 3)

	# 分配RGB buffer，用来存放ISP输出的图像
	# 备注：从相机传输到PC端的是RAW数据，在PC端通过软件ISP转为RGB数据（如果是黑白相机就不需要转换格式，但是ISP还有其它处理，所以也需要分配这个buffer）
	pFrameBuffer = mvsdk.CameraAlignMalloc(FrameBufferSize, 16)




	while (1) :
		# 从相机取一帧图片
		try:
			pRawData, FrameHead = mvsdk.CameraGetImageBuffer(hCamera, 200)
			mvsdk.CameraImageProcess(hCamera, pRawData, pFrameBuffer, FrameHead)
			mvsdk.CameraReleaseImageBuffer(hCamera, pRawData)
			
			# 此时图片已经存储在pFrameBuffer中，对于彩色相机pFrameBuffer=RGB数据，黑白相机pFrameBuffer=8位灰度数据
			# 把pFrameBuffer转换成opencv的图像格式以进行后续算法处理
			frame_data = (mvsdk.c_ubyte * FrameHead.uBytes).from_address(pFrameBuffer)
			frame = np.frombuffer(frame_data, dtype=np.uint8)
			frame = frame.reshape((FrameHead.iHeight, FrameHead.iWidth, 1 if FrameHead.uiMediaType == mvsdk.CAMERA_MEDIA_TYPE_MONO8 else 3) )
			# # 实时显示
			# cv2.imshow('frame', frame)
			#临时输出距离均值
			#BGR
			X = cv2.pyrDown(cv2.pyrDown(frame))
			#保存
			cv2.imwrite(r'E:\pycharm\camera\navigationWithZ\camera_develop\result\capture\ori.bmp',frame)
			# #图片翻转
			# frame=cv2.flip(frame,0)
			# #旋转
			w, h = frame.shape[:2]
			# print(w,h)
			M = cv2.getRotationMatrix2D((h / 2, w / 2), 180, 1)
			frame = cv2.warpAffine(frame, M, (h, w))
			# cv2.imshow('capture1',frame)
			# cv2.waitKey(0)
			# print(frame,type(frame),frame.shape)
			#深度学习框架调用
			# frame=deep_convert(frame)
			#矩阵框架
			#滤波
			frame=cv2.GaussianBlur(frame,(0,0),1.8)
			# frame=cv2.blur(frame,(5,5))
			# frame=cv2.medianBlur(frame,9)
			# frame=cv2.bilateralFilter(frame,d=0,sigmaColor=50,sigmaSpace=15)
			frame=image_input(frame)

			#临时计算距离平均
			Y = cv2.pyrDown(cv2.pyrDown(frame))
			#保存
			cv2.imwrite(r'E:\pycharm\camera\navigationWithZ\camera_develop\result\capture\correct.bmp',frame)
			#显示距离均值
			t=np.sum(((X - Y) ** 2) ** 0.5, axis=2)
			print('距离均值',np.mean(t),'距离方差',np.var(t))
			# 图片翻转
			# frame = cv2.flip(frame, 1)
			#实时显示
			#滤波
			# frame=cv2.GaussianBlur(frame,(0,0),1.8)
			# frame=cv2.blur(frame,(5,5))

			#不加投影仪时显示使用
			# frame=cv2.medianBlur(frame,3)
			# frame=cv2.bilateralFilter(frame,d=0,sigmaSpace=15,sigmaColor=100)
			# cv2.imshow('frame',frame)
			# cv2.waitKey( )

			# #相机投影之间的矫正关系
			# fx=0.4
			# fy=0.4
			# switch(waitKey(1))
			# {
			#   fx=
			#   fy=
			#    l=
			#    t=
			# default: break;
			# }
			# frame=cv2.resize(frame,None,fx=fx,fy=fy)

			#贴到背景图
			w,h,d=frame.shape
			print('shape',w,h,d)
			# frame=cv2.flip(frame,0)
			M = cv2.getRotationMatrix2D((h / 2, w / 2), 180, 1)
			frame = cv2.warpAffine(frame, M, (h, w))
			# print(w,h)
			# 起点 l,t
			# cv2.waitKey()
			# 			# t =raw_input("请输入")
			t=50
			l=50

			# ti = cv2.waitKey(33)

			# if ti == 49:
			# 	fx=fx+0.01
			# elif ti == 50:
			# 	fy = fy + 0.01
			# else:
			# 	fx=fx2
			#########
			# img = cv2.imread('360.png')
			# print(img.shape)
			# img_copy = deepcopy(frame)
			# img2 = np.zeros([800, 1280, 3], np.uint8)
			# # img2 = np.zeros((1024, 1920, 3), np.uint8)
			# img2_copy = deepcopy(img2)
			# cv2.namedWindow('image_cp',cv2.WINDOW_NORMAL)
			# cv2.resizeWindow('image_cp',640,480)
			# cv2.namedWindow('image', cv2.WINDOW_NORMAL)
			# cv2.resizeWindow('image', 640, 480)
			# cv2.namedWindow('image2', cv2.WINDOW_NORMAL)
			# cv2.resizeWindow('image2', 640, 480)
			# cv2.namedWindow('image2_cp',cv2.WINDOW_NORMAL)
			# cv2.resizeWindow('image2_cp',640,480)
			# cv2.setMouseCallback('image_0 ', draw_circle)
			# cv2.setMouseCallback('image2', copy_circle)
			##

			# img_0[l:l + w, t:t + h, 0] = frame[:, :, 0]
			# img_0[l:l + w, t:t + h, 1] = frame[:, :, 1]
			# img_0[l:l + w, t:t + h, 2] = frame[:, :, 2]

			# img_copy = deepcopy(img_0)
			# img2 = np.zeros([800, 1280, 3], np.uint8)
			# img2 = np.zeros((1024, 1920, 3), np.uint8)
			# img2_copy = deepcopy(img2)
			frame = cv2.resize(frame,(1280,800))
			dst = cv2.add(frame,img_3)
			cv2.imshow('projector0', dst)

			# 图像放大与平移
			img2=img2[0:600,0:1000,3]

			# 图像缩小（加黑边）
			cv2.copyMakeBorder(img2,0,0,0,0,cv2.BORDER_ISOLATED,img2,(0,0,0))

			cv2.imshow('projector1',img2)
			k = cv2.waitKey(1) & 0xFF
			if k == ord('m'):
				mode = not mode
			elif k == ord('q'):
				break
			# img2[l:l + w, t:t + h, 0] = frame[:, :, 0]
			# img2[l:l + w, t:t + h, 1] = frame[:, :, 1]
			# img2[l:l + w, t:t + h, 2] = frame[:, :, 2]
		    # cv2.imshow('projector', img2)
			# frame1[l:l + w, t:t + h, 0] = frame[:, :, 0]
			# frame1[l:l + w, t:t + h, 1] = frame[:, :, 1]
			# frame1[l:l + w, t:t + h, 2] = frame[:, :, 2]
			# cv2.imshow('projector', frame1)
            #########
			# # img = cv2.imread('360.png')
			# # print(img.shape)
			# img_copy = deepcopy(img_0)
			# img2 = np.zeros([800, 1280, 3], np.uint8)
			# # img2 = np.zeros((1024, 1920, 3), np.uint8)
			# img2_copy = deepcopy(img2)
			# # cv2.namedWindow('image_cp',cv2.WINDOW_NORMAL)
			# # cv2.resizeWindow('image_cp',640,480)
			# # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
			# # cv2.resizeWindow('image', 640, 480)
			# # cv2.namedWindow('image2', cv2.WINDOW_NORMAL)
			# # cv2.resizeWindow('image2', 640, 480)
			# # cv2.namedWindow('image2_cp',cv2.WINDOW_NORMAL)
			# # cv2.resizeWindow('image2_cp',640,480)
			# cv2.waitKey(200)
			# ##
		    # cv2.setMouseCallback('image_0 ', draw_circle)
		    # cv2.setMouseCallback('image2', copy_circle)

		except mvsdk.CameraException as e:
			if e.error_code != mvsdk.CAMERA_STATUS_TIME_OUT:
				print("CameraGetImageBuffer failed({}): {}".format(e.error_code, e.message) )

	# 关闭相机
	mvsdk.CameraUnInit(hCamera)

	# 释放帧缓存
	mvsdk.CameraAlignFree(pFrameBuffer)

def main():
	# cv2.setMouseCallback('projector', draw_circle)
	# cv2.setMouseCallback('projector1', copy_circle)


	try:
		main_loop()

	finally:
		cv2.destroyAllWindows()



#输出当前图的匹配度
def similarity():
	X=cv2.imread(r'F:\yuanchengshoushudaohang\camera\navigationWithZ\camera_develop\result\copy\1.png')
	Y=cv2.imread(r"F:\yuanchengshoushudaohang\camera\navigationWithZ\camera_develop\result\copy\2.png")
	X = cv2.cvtColor(X,cv2.COLOR_BGR2Lab)
	Y = cv2.cvtColor(Y, cv2.COLOR_BGR2Lab)
	t = np.sum(((X - Y) ** 2) ** 0.5, axis=2,dtype=float)
	print('均值',np.mean(t),'方差',np.var(t))
	w,h=t.shape
	d={}
	for i in range(w):
		for j in range(h):
			d[t[i][j]]=d.get(t[i][j],0)+1
	# 绘制条形图
	index = sorted(list(d.keys()))
	print(index)
	print(type(index))
	print(d)
	y = []
	for i in index:
		y.append(d[i])
	#设置字体格式
	font1 = {'family': 'Times New Roman',
			 'weight': 'normal',
			 'size': 22,
			 }
	figsize = 11, 9
	figure, ax = plt.subplots(figsize=figsize)
	#设置柱状图宽度
	# plt.bar(index, y,width=1,edgecolor = 'white')
	plt.bar(index, y,edgecolor = 'white')

	# 设置坐标刻度值的大小以及刻度值的字体
	plt.tick_params(labelsize=22)
	labels = ax.get_xticklabels() + ax.get_yticklabels()
	[label.set_fontname('Times New Roman') for label in labels]

	# plt.title('RGB')
	# plt.xlabel('两张图RGB对应的二阶距离')
	plt.xlabel('The euclidean metric of the RGB values between the original and distorted picture',font1)
	# plt.ylabel('差值出现的次数')
	plt.ylabel('The number of counts',font1)
	plt.show()


#矫正
correct()
# cv2.setMouseCallback('projector', draw_circle)
# cv2.setMouseCallback('projector1', copy_circle)
##
# #视频
main()
#匹配度
# similarity()

