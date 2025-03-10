import cv2
import numpy as np

K = None
D = None
MATRIX = None
ROI = None
SIZE = [[None, None], [None, None]]  # Сначала y, потом x


def make_matrix(k: list[list[int | float]], d: list[int | float],
                size: tuple[tuple[int, int], tuple[int, int]]) -> None:
    global K, D, MATRIX, ROI, SIZE

    SIZE = size
    K = np.array(k)
    D = np.array(d)

    width = size[1][1] - size[1][0]
    height = size[0][1] - size[0][0]

    MATRIX, ROI = cv2.getOptimalNewCameraMatrix(K, D, (height, width), 1, (height, width))


def fix_distortion(frame: np.ndarray) -> np.ndarray:
    # Перед устранением эффекта рыбьего глаза обрезаем видеовыход до желаемых значений
    # (на картинке такого разрешения работал скрипт для вычисления коэффициентов)

    frame = frame[SIZE[0][0]:SIZE[0][1], SIZE[1][0]:SIZE[1][1]]

    frame = cv2.undistort(frame, K, D, None, MATRIX)

    return frame
