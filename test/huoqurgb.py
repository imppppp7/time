import cv2
# mouse callback function
def mouseonmove(event,x,y,flags,param):
    if event == cv2.EVENT_MOUSEMOVE:
        print('图像的坐标是' , img[y,x])

# Create a black image, a window and bind the function to window
img = cv2.imread(r'C:\project\teleguidence\time\red.png')
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image',mouseonmove)
while(1):
    cv2.imshow('image',img)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
