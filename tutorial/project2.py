import cv2
import numpy as np

# Read WebCam
widthImg = 540
heightImg = 640
# cap = cv2.VideoCapture(0)   # webcam
# cap.set(3, widthImg)        # width
# cap.set(4, heightImg)       # height
# cap.set(10, 150)            # brightness

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

def preProcessing(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,200,200)
    # sometimes the edges are thin, so we will apply dilation and erosion
    # dilation is to thicken, erosion is to thin
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=2)
    imgThres = cv2.erode(imgDial,kernel,iterations=1)
    return imgThres

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    # Image, Retrieval Method (retrieve the extreme outer contours), approximation
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:        # loop through all contours
        area = cv2.contourArea(cnt) # get the area
        if area>5000:    # give minimum threshold for the area to avoid any noise
            # image, contour, -1 for all the contour, blue colour, thickness 3
            # cv2.drawContours(imgContour,cnt,-1,(255,0,0),3) # draw out the contours
            peri = cv2.arcLength(cnt,True)  # get the arc length (corners of our shape)
            # 2nd argument is the resolution
            approx = cv2.approxPolyDP(cnt,0.02*peri,True) # approximate the corner points (i.e. how many corner points we have)
            # this will give us the biggest area and biggest approximation (corners)
            if area>maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour,biggest,-1,(255,0,0),20) # draw out the contours
    return biggest  # giving us our biggest contour

# custom function for resizing image
def resize_img(img, scale):
    scale_percent = scale  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized

def reorder(myPoints):
    # Since you will get arrays of [[111,222]], [[222,333]]... etc.
    # When you add them up, the smallest one is our left corner, biggest one is our
    # the shape of biggest is (4,1,2), we have 4 diff points, and for each point we have x and y
    myPoints = myPoints.reshape((4,2))  # so we're removing that 1
    # create a new matrix that we will send outside that we will return to the function
    myPointsNew = np.zeros((4,1,2),np.int32)
    # the output is something like [238 340 651 488]
    add = myPoints.sum(1)   # this will add the matrix up, i.e. [[111,222]] will become [333]
    myPointsNew[0] = myPoints[np.argmin(add)]   # we will set our smallest value to be the first index
    myPointsNew[3] = myPoints[np.argmax(add)]   # largest value
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]  # set the 2nd
    myPointsNew[2] = myPoints[np.argmax(diff)]  # and the 3rd values
    return myPointsNew


def getWarp(img,biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    # the value may change based on the angle of the paper, and the contour
    # so we need to arrange the biggest points before we send it for warping
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    return imgOutput
    # crop the edges a little
    imgCropped = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped, (widthImg, heightImg))
    return imgCropped


# cv2.resize(img,(widthImg,heightImg))
img = cv2.imread("../Resources/1.jpg")
img = cv2.resize(img, (widthImg, heightImg))
imgContour = img.copy()
imgThres = preProcessing(img)
biggest = getContours(imgThres)
if biggest.size != 0:
    imgWarp = getWarp(img,biggest)
    imageArray = ([img,imgThres],
              [imgContour,imgWarp])
else:
    imageArray = ([img, imgThres],
                  [img, img])
stackedImages = stackImages(0.4,imageArray)
cv2.imshow("WorkFlow", stackedImages)
imgWarp = resize_img(imgWarp,80)
cv2.imshow("ImageWarped", imgWarp)
cv2.waitKey(0)
