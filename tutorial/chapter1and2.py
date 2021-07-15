import cv2
import numpy as np

img = cv2.imread("../Resources/imda-logo.png")         # load the image
# 5 x 5 matrix with all ones, np.uint8 means (8 bits) the values can range from 0 to 255
kernel = np.ones((5,5), np.uint8)

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     # gray the image
# 2nd argument is the kernel, defines how blur it is, the value must be an odd number
# i.e. 3,3 is okay, 5,5 is okay etc.
imgBlur = cv2.GaussianBlur(imgGray,(7,7), 0)        # blur the image
imgCanny = cv2.Canny(img, 300, 300)                 # edge detector
print(imgCanny.shape)
print(imgBlur.shape)
# a kernel is just a matrix which we have to define the size and value of
# in this case, we need a matrix with all 1 values, but we need to define the size
# iteration = 1 means how thick do we want it to be (multiple iteration means you keep running it)
imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)    # thicken the image (we use the canny image to thicken the edges)
imgErosion = cv2.erode(imgDilation, kernel, iterations=1)   # thin the image

# cv2.imshow("Gray Image", imgGray)                   # display the image
# cv2.imshow("Blur Image", imgBlur)
cv2.imshow("Canny Image", imgCanny)
cv2.imshow("Dilation Image", imgDilation)
cv2.imshow("Erosion Image", imgErosion)
cv2.waitKey(0)  # wait for x seconds before the image vanish