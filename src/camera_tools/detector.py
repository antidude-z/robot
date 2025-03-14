import cv2
import numpy as np


class DetectableObject:
    def __init__(self, blur_val: int, lowerb: list, upperb: list, ksize: int, area: int = 1000,
                 morph=cv2.MORPH_RECT):
        self.blur = blur_val
        self.lowerb = lowerb
        self.upperb = upperb
        self.ksize = ksize
        self.area = area
        self.morph = morph

    def proceed(self, frame, show_contours=False):
        mask = cv2.medianBlur(frame, 1 + self.blur * 2)
        mask = cv2.inRange(mask, np.array(self.lowerb), np.array(self.upperb))
        kernel = cv2.getStructuringElement(self.morph, (self.ksize, self.ksize))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

        edged = cv2.Canny(mask, 50, 150, apertureSize=3, L2gradient=True)

        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, )

        for i in range(len(contours)):
            if cv2.contourArea(contours[i]) > self.area:
                frame = cv2.drawContours(frame, contours[i], -1, (0, 255, 0), 3)
                M = cv2.moments(contours[i])
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                cv2.putText(frame, f'{i}_({cx}:{cy})', (cx + 10, cy - 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 255, 255), 1)

        if show_contours:
            return edged

        return frame
