import cv2
import numpy as np

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

img = cv2.imread("../Resources/shapes.png")

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# higher sigma (last argument) - more blur it gets
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur,100,100)
imgBlank = np.zeros_like(img)
imgContour = img.copy()
def getContours(img):
    # Image, Retrieval Method (retrieve the extreme outer contours), approximation
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:        # loop through all contours
        area = cv2.contourArea(cnt) # get the area
        print(area)
        if area>500:    # give minimum threshold for the area to avoid any noise
            # image, contour, -1 for all the contour, blue colour, thickness 3
            cv2.drawContours(imgContour,cnt,-1,(255,0,0),3) # draw out the contours
            peri = cv2.arcLength(cnt,True)  # get the arc length (corners of our shape)
            print(peri) # The true above and below means that the shape is closed
            # 2nd argument is the resolution
            approx = cv2.approxPolyDP(cnt,0.02*peri,True) # approximate the corner points (i.e. how many corner points we have)
            print(len(approx))  # this is number of corners it has, i.e. 3 is triangle
            print(approx)       # approx is the x y coordinates i believe
            objCor = len(approx)
            # this will give you the x y and the width and height of the object
            x, y, w, h = cv2.boundingRect(approx)

            if objCor==3 : objectType = "Tri"
            elif objCor == 4:   # it can either be rectangle or square
                aspRatio = w/float(h)   # the aspect ratio of square should be 1
                if aspRatio > 0.95 and aspRatio < 1.05: # allow deviation of 5%
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objCor>4:objectType="Circle"
            else:objectType=None

            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)  # drawing the bounding boxes
            # put it near the center of the object, center minus 10 pixels
            cv2.putText(imgContour, objectType,
                        (x+(w//2)-10,y+(h//2)-10),        # putting text near the center
                        cv2.FONT_HERSHEY_COMPLEX,0.8,   # font + scale
                        (0,0,0),2)                  # colour + thickness
getContours(imgCanny)

imgStack = stackImages(0.4, ([img,imgGray,imgBlur],[img,imgContour,imgBlank]))
cv2.imshow("Image", imgStack)
cv2.waitKey(0)