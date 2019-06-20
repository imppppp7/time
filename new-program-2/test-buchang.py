import numpy as np
import cv2
from camera1 import Camera
from matplotlib import pyplot as plt


def ORB(img):
    # Initiate FAST object with default values
    orb = cv2.ORB_create()
    # find and draw the keypoints
    kp = orb.detect(img, None)
    kp, des = orb.compute(img, kp)
    img1 = cv2.drawKeypoints(img, kp, None, color=(255, 0, 0))
    cv2.imshow('1', img1)
    cv2.waitKey(10)
# cv2.BFMatcher


def orb_bfmatching():
    img1 = cv2.imread('image1.BMP')
    img2 = cv2.imread('image2.BMP')
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('1',img1)
    # cv2.waitKey()
    # orb = cv2.FastFeatureDetector_create()
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1, des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)
    # Draw first 10 matches.
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:4], None, flags=2)
    plt.imshow(img3), plt.show()

# orb_bfmatching()


def orb_bfmatching_2():
    img1 = cv2.imread('image1.BMP')
    img2 = cv2.imread('image2.BMP')
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('1',img1)
    # cv2.waitKey()
    # orb = cv2.FastFeatureDetector_create()
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    # FLANN parameters
    FLANN_INDEX_LSH = 0
    index_params = dict(algorithm=FLANN_INDEX_LSH,
                        table_number=6,  # 12
                        key_size=12,  # 20
                        multi_probe_level=1)  # 2
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]
    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matchesMask[i] = [1, 0]
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=0)
    img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, matches, None, **draw_params)
    plt.imshow(img3, ), plt.show()


# orb_bfmatching_2()

# 光流法
# 实例化相机
# Cam = Camera()
# # while 1:
# #     frame = Cam.run()
# #     frame1 = cv2.flip(frame, 0)
#
# # params for ShiTomasi corner detection
# feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
#
# # Parameters for lucas kanade optical flow
# lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
#
# # Create some random colors
# color = np.random.randint(0, 255, (100, 3))
#
# # Take first frame and find corners in it
# old_frame = Cam.run()
# old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
# p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
#
# # Create a mask image for drawing purposes
# mask = np.zeros_like(old_frame)
#
# while 1:
#     frame = Cam.run()
#     frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     # calculate optical flow
#     p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
#
#     # Select good points
#     good_new = p1[st == 1]
#     good_old = p0[st == 1]
#
#     # draw the tracks
#     for i, (new, old) in enumerate(zip(good_new, good_old)):
#         a, b = new.ravel()
#         c, d = old.ravel()
#         mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
#         frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)
#     img = cv2.add(frame, mask)
#
#     cv2.imshow('frame', img)
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#
#     # Now update the previous frame and previous points
#     old_gray = frame_gray.copy()
#     p0 = good_new.reshape(-1, 1, 2)


