import cv2
import numpy as np
import math


class DetectableObject:
    def __init__(self, blur_val: int, lowerb: list, upperb: list, ksize: int, area: int = 1000,
                 morph=cv2.MORPH_RECT, single: bool = False):
        self.blur = blur_val
        self.lowerb = lowerb
        self.upperb = upperb
        self.ksize = ksize
        self.area = area
        self.morph = morph
        self.single = single

        self.avg_x = []
        self.avg_y = []

    def proceed(self, frame, show_contours=False):
        odd_blur = 1 + self.blur * 2
        mask = cv2.medianBlur(frame, odd_blur)

        mask = cv2.inRange(mask, np.array(self.lowerb), np.array(self.upperb))
        kernel = cv2.getStructuringElement(self.morph, (self.ksize, self.ksize))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

        edged = cv2.Canny(mask, 50, 150, apertureSize=5, L2gradient=True)

        contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        coords = []

        for i in range(len(contours)):
            if cv2.contourArea(contours[i]) < self.area:
                continue

            M = cv2.moments(contours[i])
            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])

                if self.single:
                    cx1 = sum(self.avg_x) / max(len(self.avg_x), 1)
                    cy1 = sum(self.avg_y) / max(len(self.avg_y), 1)

                    distance = math.sqrt((cx - cx1) ** 2 + (cy - cy1) ** 2)

                    if distance > 50 and len(self.avg_x) > 0:
                        continue

                    if len(self.avg_x) <= 10:
                        self.avg_x.append(cx)
                        self.avg_y.append(cy)

                    if len(self.avg_x) == 10:
                        self.avg_x.pop(0)
                        self.avg_y.pop(0)

            frame = cv2.drawContours(frame, contours[i], -1, (0, 255, 0), thickness=3)

            frame = cv2.fillPoly(frame, [contours[i]], color=(255, 255, 255))
            kernel = np.ones((7, 7), np.uint8)
            frame_dil = cv2.dilate(frame, kernel, iterations=1)

            cv2.putText(frame, f'{i}_({cx}:{cy})', (cx + 10, cy - 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 1)
            coords.append((cx, cy))

            if self.single:
                break

        if show_contours:
            return edged, coords

        return frame, frame_dil, coords
