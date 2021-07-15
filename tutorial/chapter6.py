import cv2
import numpy as np
# Goal is to show image side by side

img = cv2.imread("../Resources/Lena.png")
# to put 2 images side by side
imgHor = np.hstack((img,img))   # horizontal stack
imgVer = np.vstack((img,img))   # vertical stack
# issues with this method
# 1) We cannot resize the images
# 2) If the 2 images do not have the same channel, i.e. 1 is rgb, 1 is gray
# it does not work. Since we're stacking matrices

# heres the solution
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgHStack = stackImages(0.5, [img,img,img])  # horiozntal stack
# if you have 3 columns in the first row, you need to have 3 columns in the 2nd
imgVStack = stackImages(0.5, ([img,img,img],[img,img,img]))  # vertical stack
# you can stack images with different colour as well
imgVColouredStack = stackImages(0.5, ([imgGray,img,imgGray],[img,imgGray,img]))  # vertical stack

# cv2.imshow("Horizontal", imgHor)
# cv2.imshow("Vertical", imgVer)
cv2.imshow("Image Horizontal Stack", imgHStack)
cv2.imshow("Image Vertical Stack", imgVStack)
cv2.imshow("Image Vertical Coloured Stack", imgVColouredStack)
cv2.waitKey(0)