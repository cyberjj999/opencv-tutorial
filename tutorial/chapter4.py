import cv2
import numpy as np

# 0 means black, 512 x 512 is the size
grayscaleImg = np.zeros((512, 512)) # grayscale image
print(grayscaleImg.shape)
# new argument gives the value of 0 to 255
colouredImg = np.zeros((512, 512, 3), np.uint8) # coloured image
# make the image blue, the colon represent the entire pixel
colouredImg[:] = 255, 0, 0  # since cv2 uses BGR (Blue, Green, Red)
# heres another example to make part of the image red
colouredImg[200:300, 100:300] = 0, 0, 255

# drawing shapes
img = np.zeros((512, 512, 3), np.uint8) # coloured image
# arguments are image, starting point, ending point, colour, thickness of line
cv2.line(img, (0,0), (300,300), (0,255,0), 3)   # draw a line
# img.shape returns i.e. (120, 200, 3), which are the height, width and channels
# to get the height, you use img.shape[0], the width you use img.shape[1] etc.
# to draw a line across the whole image, you can use the argument below
cv2.line(img, (0,0), (img.shape[1],img.shape[0]), (0,255,0), 3)  # confusing because width x height vs height x width
# same arguments as above, but instead it draws a rectangle
cv2.rectangle(img, (0,0), (250,350), (0,0,255), 2)  # draw a rectangle
# if you want to fill the entire rectangle, instead of specifying extreme thickness
cv2.rectangle(img, (0,0), (50,50), (255,0,0), cv2.FILLED) # you can use cv2.filled
# argument: image, center point, radius, colour, thickness
cv2.circle(img, (400,50), 30, (255,255,0), 5)   # draw a circle
# argument: image, text, origin (starting pt), font, scale, colour, thickness
# scale is how big it is, i.e. 10x scale means 10 times the size
cv2.putText(img, " OPENCV ", (300, 150), cv2.FONT_ITALIC, 1, (255, 255, 255), 3)

cv2.imshow("Image", img)
# cv2.imshow("Gray Scale Image", grayscaleImg)
# cv2.imshow("Coloured Image", colouredImg)

cv2.waitKey(0)