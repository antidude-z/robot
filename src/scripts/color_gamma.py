import cv2
from src.camera_tools import sliders


sliders.create_window(500, 300)
sliders.create_multiple_settings([('b1', 0, 255, 0), ('g1', 0, 255, 0), ('r1', 88, 255, 0),
                                  ('b2', 148, 255, 0), ('g2', 158, 255, 0), ('r2', 255, 255, 0)])


img = cv2.imread("spektor.png")

while True:
    r1, g1, b1, r2, g2, b2 = sliders.gather('r1', 'g1', 'b1', 'r2', 'g2', 'b2')

    min_p = (b1, g1, r1)
    max_p = (b2, g2, r2)

    img_g = cv2.inRange(img, min_p, max_p)
    result = cv2.bitwise_and(img, img, mask=img_g)

    cv2.imshow("or", img)
    cv2.imshow("mask", img_g)
    cv2.imshow("result", result)

    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
