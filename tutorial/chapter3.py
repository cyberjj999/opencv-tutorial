import cv2
import numpy as np

img = cv2.imread("../Resources/lambo.png")         # load the image
# output: (1500, 2000, 3)
# (rows (height), columns (width), channels - BGR)
print(img.shape)
# width, height of the new size
imgResize = cv2.resize(img, (300, 200))         # resize the image
print(imgResize.shape)
# a little tricky since image is height by width, but open cv uses width by height
# what we can do here is to only take the image height of 0-200 pixels
# and width of 200 to 500 pixels.
# good to note that the height 0-200 is from top to bottom, since thats how opencv track images
imgCropped = img[0:200, 200:500]    # no need to use cv2, can just manipulate the matrix
# image is just a matrix, or an array of pixels

cv2.imshow("Image", img)
cv2.imshow("Image Resized", imgResize)
cv2.imshow("Image Cropped", imgCropped)
cv2.waitKey(0)