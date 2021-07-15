import cv2
import numpy as np
# The logic is that the cascade contain many positive faces and negative faces
# In other words, there are many real faces and many other things that are not faces, so they can clearly detect faces
faceCascade = cv2.CascadeClassifier("Resources/haarcascades/haarcascade_frontalface_default.xml")
img = cv2.imread("../Resources/Lena.png")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray image, scale factor and minimum neighbours
faces = faceCascade.detectMultiScale(imgGray, 1.1, 4) # this will detect multiple faces
# drawing bbox on the faces detected
for (x,y,w,h) in faces:
    # initial points, corner points
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

# Not the most accurate but it is fast and works well in some circumstances
cv2.imshow("Image", img)
cv2.waitKey(0)

# Detection of Face