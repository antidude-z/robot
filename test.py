import cv2
img = cv2.imread("images/frame0.png")
#центр 639, 479 - 640, 480
#края 246, 86 - 1033, 873
crop_img = img[86:873, 246:1033]
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)