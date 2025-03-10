"""Файл конфигурации.
Позволяет не трогать другой код в 90% случаев (до тех пор, пока не потребуется новая фича/скрипт).
"""
import numpy as np

from src.camera_tools.input_source import InputSource

NORMALIZE_OUTPUT: bool = True
ADJUST_COEFFS_REALTIME: bool = False
INPUT_SOURCE: InputSource = InputSource.VIDEO

NORMALIZED_DIMENSIONS = ((700, 1150), (700, 1850))
DEFAULT_K = [[529, 0, 585], [4, 482, 241], [0, 0, 1]]
DEFAULT_D = [-292, 106, 0, 0, -21]

RTSP_URL = "rtsp://admin:UrFU_ISIT@10.32.9.223:554/Streaming/channels/101"
VIDEO_SOURCE_PATH = 'video/robotCam_tst_video.avi'
IMAGE_SOURCE_PATH = 'images/*'

VIDEO_FILE_OUTPUT: bool = True
VIDEO_OUTPUT_PATH = 'video/test.avi'
IMAGE_FILE_OUTPUT: bool = False
IMAGE_OUTPUT_PATH = 'dataset/'

FPS: int = 1000

CUBE_DETECTION_MODE: bool = False
SHOW_CONTOURS: bool = False

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
