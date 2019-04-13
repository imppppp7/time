import cv2
import screeninfo
import numpy as np


def projector(id,picture):
	screen_id=id
	img_0 = np.zeros([800, 1280, 3], np.uint8)
	img_1 = np.zeros([800, 1280, 3], np.uint8)

	# get the size of the screen
	screen=screeninfo.get_monitors()[screen_id]
	width,height=screen.width,screen.height
	print('w,d',width,height)

	#全屏显示
	cv2.namedWindow('projector%d' %id, cv2.WINDOW_AUTOSIZE)
	cv2.moveWindow('projector%d'%id, screen.x, screen.y)
	# cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
	if id == 0:
		cv2.imshow('projector%d'%id, cv2.add(img_0,picture))
	elif id == 1:
		cv2.imshow('projector%d' % id, cv2.add(img_1, picture))