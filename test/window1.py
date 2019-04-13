import cv2
import screeninfo
import numpy as np
import copy


class Window:
	def __init__(self,windowname):
		self.windowname = windowname
		self.image = np.zeros([800, 1280, 3], np.uint8)
		self.image_copy = np.zeros([800, 1280, 3], np.uint8)
		self.mode = True
		self.drawing = False
		self.x
		self.y

	def createwindow(self,width,height):
		cv2.namedWindow(self.windowname,cv2.WINDOW_NORMAL)
		cv2.resizeWindow(self.windowname,width,height)

	def showimage(self):
			cv2.imshow(self.windowname,self.image)

	def addimage(self,image2):
		self.image = cv2.add(self.image,image2)
		self.image_copy = copy.copy(self.image)

	def movewindow(self,id):
		screen_id=id
		screen=screeninfo.get_monitors()[screen_id]
		width,height=screen.width,screen.height
		print('width,height are ',width,height)
		cv2.moveWindow(self.windowname,screen.x,screen.y)

	def bindingwi(self,color):
		def drawcircle(event,x,y,flags,param):
			if event == cv2.EVENT_LBUTTONDOWN:
				self.drawing = True
			elif event == cv2.EVENT_MOUSEMOVE:
				if self.drawing == True:
					if self.mode == True:
						cv2.circle(self.image, (x, y), 4,color, -1)
					else:
						self.image[y - 25:y + 25, x - 25:x + 25, :] = self.image_copy[y - 25:y + 25, x - 25:x + 25, :]
			elif event == cv2.EVENT_LBUTTONUP:
				self.drawing = False
			return x,y
		cv2.setMouseCallback(self.windowname,drawcircle)