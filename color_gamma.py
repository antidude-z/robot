import cv2
import numpy as np

#cap = cv2.VideoCapture("C:/Users/admin/Desktop/Mash/robotCam_1.avi")
#cap = cv2.VideoCapture(0)

def nothing(args): pass

cv2.namedWindow("setup")
cv2.createTrackbar("b1", "setup", 0, 255, nothing)
cv2.createTrackbar("g1", "setup", 0, 255, nothing)
cv2.createTrackbar("r1", "setup", 88, 255, nothing)
cv2.createTrackbar("b2", "setup", 148, 255, nothing)
cv2.createTrackbar("g2", "setup", 158, 255, nothing)
cv2.createTrackbar("r2", "setup", 255, 255, nothing)

fn = "theory/spektor.png"
img = cv2.imread(fn)


while True:
    
    r1 = cv2.getTrackbarPos('r1', 'setup')
    g1 = cv2.getTrackbarPos('g1', 'setup')
    b1 = cv2.getTrackbarPos('b1', 'setup')
    r2 = cv2.getTrackbarPos('r2', 'setup')
    g2 = cv2.getTrackbarPos('g2', 'setup')
    b2 = cv2.getTrackbarPos('b2', 'setup')

    min_p = (b1, g1, r1)
    max_p = (b2, g2, r2)

    img_g = cv2.inRange(img, min_p, max_p)
    result = cv2.bitwise_and(img, img, mask=img_g)

    cv2.imshow("or", img)
    cv2.imshow("mask", img_g)
    cv2.imshow("result", result)

    if cv2.waitKey(33) & 0xFF == ord('q'):
         break

fn.release()
cv2.destroyAllWindows()