"""Файл конфигурации.
Позволяет не трогать другой код в 90% случаев (до тех пор, пока не потребуется новая фича/скрипт).
"""
from src.camera_tools.input_source import InputSource
from src.camera_tools.detector import DetectableObject

FPS: float = 1000  # Скорость обработки кадров (не всегда точно соотв. значению)

# 1. "Нормализация" видеовыхода -> исправление эффекта рыбьего глаза и обрезание/масштабирование картинки

# NORMALIZE_OUTPUT: True - включить нормализацию. False - необработанное видео с камеры
# FISHEYE_DIMENSIONS: изображение обрезается до этих границ перед исправлением дисторсии
# NORMALIZED_DIMENSIONS: после исправления дисторсии производится доп. обрезка
# NORMALIZED_RESIZE_RATE: во сколько раз масштабировать результирующую картинку

NORMALIZE_OUTPUT: bool = True
FISHEYE_DIMENSIONS: tuple = ((700, 1150), (700, 1850))
NORMALIZED_DIMENSIONS: tuple = ((150, 350), (150, 850))
NORMALIZED_RESIZE_RATE: float = 2

# 2. Коэффициенты для исправления эффекта рыбьего глаза (дисторсии)

# DEFAULT_K: стандартные коэффициенты матрицы в виде [[a1, a2, a3], [b1, b2, b3], [c1, c2, c3]]
# DEFAULT_D: стандартные коэффициенты искажения в виде [d1, d2, d3, d4, d5]

DEFAULT_K: list[list[int]] = [[529, 0, 585], [4, 482, 241], [0, 0, 1]]
DEFAULT_D: list[int] = [-292, 106, 0, 0, -21]

# 3. Настройка коэффициентов в режиме реального времени

# ADJUST_COEFFS_REALTIME: True - появится отдельное окно со слайдерами для подгона значений
# K_RANGE, D_RANGE - предельные значения параметров K и D на слайдерах (как в сторону +, так и -)

ADJUST_COEFFS_REALTIME: bool = False
K_RANGE: int = 1000
D_RANGE: int = 300

# 4. Конфигурация источника

# INPUT_SOURCE: тип источника - камера (в режиме реального времени), заранее подготовленное видео или фотографии
# RTSP_URL: если InputSource.REALTIME, то задает адрес видеопотока камеры
# VIDEO_SOURCE_PATH: если InputSource.VIDEO, задаёт путь к видеофайлу
# IMAGE_SOURCE_PATH: если InputSource.IMAGE, задаёт путь к одному кадру или каталогу с кадрами (glob support)

INPUT_SOURCE: InputSource = InputSource.VIDEO

RTSP_URL: str = "rtsp://admin:UrFU_ISIT@10.32.9.223:554/Streaming/channels/101"
VIDEO_SOURCE_PATH: str = 'video/robotCam_tst_video3.avi'
IMAGE_SOURCE_PATH: str = 'images/*'

# 5. Формат записи видеопотока.

# VIDEO_FILE_OUTPUT: True - сохранять запись в видеофайл.
# VIDEO_OUTPUT_PATH: путь к видеофайлу.
# IMAGE_FILE_OUTPUT: True - сохранять раскадровку в указанный каталог.
# IMAGE_OUTPUT_PATH: путь к каталогу с кадрами.

VIDEO_FILE_OUTPUT: bool = False
VIDEO_OUTPUT_PATH: str = 'video/new_alg.mp4'

IMAGE_FILE_OUTPUT: bool = False
IMAGE_OUTPUT_PATH: str = 'dataset/'

# 6. Режим распознавания объектов (могут быть баги?)

# DETECTION_DEMO: True - включить вспомогательное окно для подбора параметров распознавания объекта
# DETECTION_MODE: True - объекты из OBJECTS будут распознаны при обработке кадра
# SHOW_CONTOURS: True - будут показаны только контуры найденных объектов
# OBJECTS: словарь обнаруживаемых объектов

DETECTION_DEMO: bool = False
DETECTION_MODE: bool = True
SHOW_CONTOURS: bool = False

OBJECTS = {'cone': DetectableObject(10, [0, 0, 88], [85, 65, 255], 10, area=1200),
           # 'green': DetectableObject(4, [0, 50, 0], [80, 255, 80], 5),
           'robot': DetectableObject(18, [10, 0, 0], [255, 118, 118], 12, area=1300,
                                     single=True)}  # blur 15
