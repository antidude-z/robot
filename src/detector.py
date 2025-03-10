import cv2

from src.camera_tools import sliders
from src.config import *


def create_detector_slides():
    sliders.create_window()
    # TODO
    sliders.create_multiple_settings([('FPS', 40, 400, 0), ('blue_lower', 0, 255, 0), ('green_lower', 50, 255, 0),
                                      ('red_lower', 0, 255, 0), ('blue_upper', 75, 255, 0), ('green_upper', 255, 255, 0),
                                      ('red_upper', 50, 255, 0), ('blur', 3, 30, 0), ('ksize', 30, 50, 0)])


def detect_cubes(frame):
    blur_val, ksize = sliders.gather('blur', 'ksize')
    lowerb = np.array(sliders.gather('blue_lower', 'green_lower', 'red_lower'))
    upperb = np.array(sliders.gather('blue_upper', 'green_upper', 'red_upper'))

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

    return frame, edged
