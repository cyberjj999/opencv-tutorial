import cv2
import numpy as np
# Goal is to detect colour

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

# because we don't know the min and max value for the orange colour we want to detect
# we will introduce this feature call trackbar to find the value in real time
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
# this functions run whenver the trackbar changes
def empty(a):
    pass
# Argument #1: The name for the first value we're changing (can be anything)
# Argument #2: Which window are we going to put the trackbar on
# Argument #3: Current value (the initial value when the script run)
# Argument #4: Maximum value of hue (hue is up to 360, opencv is up to 179)
# Argument #5: The function that runs everytime the user change the trackbar
cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)       # the max should be 179
# we need 6 of these, for hue, saturation, value min max    # changes were made for colour detection
cv2.createTrackbar("Hue Max","TrackBars",19,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",110,255,empty)       # the max should be 255
cv2.createTrackbar("Sat Max","TrackBars",245,255,empty)
cv2.createTrackbar("Val Min","TrackBars",153,255,empty)       # the max should be 255
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)

# in order to get the value, we need to put it in a loop
while True:
    img = cv2.imread("../Resources/lambo.png")
    # hsv is a colour scheme that stands for
    # hue, saturation, value
    # Hue is the color portion of the mode
    # Saturation describes the amount of gray in a particular color, from 0 to 100 percent.
    # Value works in conjunction with saturation and describes the brightness or intensity of the color, from 0 to 100 percent
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # we can then get the value of the trackbar and use it to apply the value to our car
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    # print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = np.array([h_min,s_min,v_min])   # an array with all min vlaue
    upper = np.array([h_max, s_max, v_max]) # ana rray with all max value
    # this will give us the filtered image of the colour
    mask = cv2.inRange(imgHSV,lower,upper)
    # this would add 2 images together to create a new image
    # if both pixel are present they will take it as a 1 and store in a new image
    imgResult = cv2.bitwise_and(img,img,mask=mask)

    # cv2.imshow("Original", img)
    # cv2.imshow("HSV Image", imgHSV)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("Result", imgResult)
    imgStack = stackImages(0.6,([img,imgHSV],[mask,imgResult]))
    cv2.imshow("Stacked Images", imgStack)
    cv2.waitKey(1)


# cv2.imshow("Image", img)
# cv2.imshow("HSV Image", imgHSV)
# cv2.waitKey(0)