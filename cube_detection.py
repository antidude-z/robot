import cv2
import numpy as np


def color_selection(color:str, L_limit:list, U_limit:list, frame):
    mask = cv2.inRange(frame, L_limit, U_limit)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    edged = cv2.Canny(mask, 50, 150, apertureSize=3)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea,)
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > 2000:
            cv2.drawContours(frame, contours[i], -1, (0, 255, 0), 3)
            M = cv2.moments(contours[i])
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
            cv2.putText(frame, str(i) + color + '_(' + str(cx) + ':' + str(cy) + ')', (cx + 10, cy - 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
            

cap = cv2.VideoCapture("C:/Users/admin/Desktop/Mash/robotCam_1.avi")
fourcc = cv2.VideoWriter.fourcc(*'MP4V')
out = cv2.VideoWriter('robotCam_tst.avi', fourcc, 20.0, (640, 480))

#red
L_limit_red = np.array([0, 0, 88])
U_limit_red = np.array([90, 90, 255])

#green
L_limit_green = np.array([0, 50, 0])
U_limit_green = np.array([80, 255, 80])

#blue
#L_limit_blue = np.array([30, 0, 0])
#U_limit_blue = np.array([255, 50, 50])

n = 0
while True:
    ret, frame = cap.read()
    frame = cv2.medianBlur(frame, 9)

    cv2.imshow('original', frame)

    color_selection('RED', L_limit_red, U_limit_red, frame)
    color_selection('GREEN', L_limit_green, U_limit_green, frame)
    #color_selection('BLUE', L_limit_blue, U_limit_blue, frame)

    out.write(frame)
    cv2.imshow("result", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()