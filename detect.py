import cv2
import numpy as np

cap = cv2.VideoCapture('video/robotCam_1.avi')
# fourcc = cv2.VideoWriter.fourcc(*'MP4V')
# out = cv2.VideoWriter('robotCam_tst.avi', fourcc, 20.0, (640, 480))

# РЕФЕРЕНСНЫЕ ЗНАЧЕНИЯ (не финальный вариант)
# red
L_limit_red = np.array([0, 0, 88])
U_limit_red = np.array([90, 90, 255])

# green
L_limit_green = np.array([0, 50, 0])
U_limit_green = np.array([80, 255, 80])

# blue
L_limit_blue = np.array([30, 0, 0])
U_limit_blue = np.array([255, 50, 50])


def nothing(n: int) -> None:
    pass


def get_setting(field):
    return cv2.getTrackbarPos(field, 'settings')


def create_setting(name, value, count):
    cv2.createTrackbar(name, 'settings', value, count, nothing)


cv2.namedWindow('settings', cv2.WINDOW_NORMAL)
cv2.resizeWindow('settings', 900, 500)
create_setting('FPS', 40, 400)
create_setting('blue_lower', 0, 255)
create_setting('green_lower', 50, 255)
create_setting('red_lower', 0, 255)
create_setting('blue_upper', 75, 255)
create_setting('green_upper', 255, 255)
create_setting('red_upper', 50, 255)
create_setting('blur', 3, 30)
create_setting('ksize', 30, 50)

while True:
    FPS = get_setting('FPS')
    lowerb = np.array([get_setting('blue_lower'), get_setting('green_lower'), get_setting('red_lower')])
    upperb = np.array([get_setting('blue_upper'), get_setting('green_upper'), get_setting('red_upper')])
    blur_val = get_setting('blur')
    ksize = get_setting('ksize')

    if FPS != 0:
        ret, frame = cap.read()

    mask = cv2.medianBlur(frame, 1 + blur_val * 2)
    mask = cv2.inRange(mask, lowerb, upperb)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

    edged = cv2.Canny(mask, 50, 150, apertureSize=3, L2gradient=True)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, )

    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > 1000:
            frame = cv2.drawContours(frame, contours[i], -1, (0, 255, 0), 3)
            M = cv2.moments(contours[i])
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
            cv2.putText(frame, f'{i}_({cx}:{cy})', (cx + 10, cy - 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 1)

    if FPS != 0:
        cv2.imshow('video feed', frame)
        # out.write(frame)

    if cv2.waitKey(max(1000 // max(FPS, 1), 1)) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
