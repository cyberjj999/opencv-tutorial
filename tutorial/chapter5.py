import cv2
import numpy as np

# objective, for the 4 cards on the desk in the image,
# we will extract out the king of spade
# and show it as flat as possible on the table
img = cv2.imread("../Resources/cards.jpg")

# playing card is usually 2.5 by 3.5 inches
width, height = 250,350 # keep the aspect ratio
# these are the coordinates to the 4 points of the card
# he hardcoded these values (can get from ms paint he say)
pts1 = np.float32([[111, 219],[287,188],[154,482],[352,440]])
# we need to specify which points refer to which corner
# i.e. first coordinate is for top left, second is for top right etc.
# this is top left, top right, btm left, btm right
pts2 = np.float32([[0, 0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1, pts2)
imgOutput = cv2.warpPerspective(img, matrix, (width, height))

cv2.imshow("Image", img)
cv2.imshow("Wrapped Image", imgOutput)
cv2.waitKey(0)

imgOutput.cv2.warpPerspective(img)