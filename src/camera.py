import cv2
import glob

from src.camera_tools import undistort, sliders
from detector import create_detector_slides, detect_cubes
from config import *

cap = files = None
if INPUT_SOURCE == InputSource.REALTIME:
    cap = cv2.VideoCapture(RTSP_URL)

    if not cap.isOpened():
        print("Ошибка: Не удалось подключиться к камере")
        exit()
elif INPUT_SOURCE == InputSource.VIDEO:
    cap = cv2.VideoCapture(VIDEO_SOURCE_PATH)
elif INPUT_SOURCE == InputSource.IMAGE:
    files = glob.iglob(IMAGE_SOURCE_PATH)

if VIDEO_FILE_OUTPUT:
    fourcc = cv2.VideoWriter.fourcc(*'mp4v')

    if NORMALIZE_OUTPUT:
        size = (1400, 400)  # TODO
    else:
        size = (2560, 1440)  # TODO

    out = cv2.VideoWriter(VIDEO_OUTPUT_PATH, fourcc, 20.0, size)

if IMAGE_FILE_OUTPUT:
    def gen_next_number():
        n = 0
        while True:
            n += 1
            yield n


    gen = gen_next_number()

if ADJUST_COEFFS_REALTIME and not CUBE_DETECTION_MODE:
    sliders.create_window()

    settings = []
    symbols = ['a', 'b', 'c']

    for i in range(4):
        if i < 3:
            for k in range(3):
                settings.append((f'{symbols[i]}{k + 1}', DEFAULT_K[i][k], 1000))  # TODO
        else:
            for k in range(5):
                settings.append((f'd{k + 1}', DEFAULT_D[k], 300))  # TODO

    sliders.create_multiple_settings(settings)
else:
    undistort.make_matrix(DEFAULT_K, list(map(lambda x: x / 1000, DEFAULT_D)), NORMALIZED_DIMENSIONS)

if CUBE_DETECTION_MODE:
    create_detector_slides()


def handle_input():
    if INPUT_SOURCE in [InputSource.REALTIME, InputSource.VIDEO]:
        ret, next_frame = cap.read()

        if not ret:
            print("Ошибка: Не удалось получить кадр")
            return None

        return next_frame
    elif INPUT_SOURCE == InputSource.IMAGE:
        try:
            return cv2.imread(next(files), cv2.IMREAD_COLOR)
        except StopIteration:
            return None


def handle_output(out_frame):
    if VIDEO_FILE_OUTPUT:
        out.write(out_frame)

    if IMAGE_FILE_OUTPUT:
        cv2.imwrite(IMAGE_OUTPUT_PATH + f'img{next(gen)}.png', out_frame)

    # Отображаем кадр в окне
    cv2.imshow('Ceiling IP Camera Stream', out_frame)


def normalize(original_frame):
    if ADJUST_COEFFS_REALTIME and not CUBE_DETECTION_MODE:
        k = [sliders.gather(f'{s}1', f'{s}2', f'{s}3') for s in ('a', 'b', 'c')]
        d = list(map(lambda x: x / 1000, sliders.gather('d1', 'd2', 'd3', 'd4', 'd5')))

        undistort.make_matrix(k, d, NORMALIZED_DIMENSIONS)

    new_frame = undistort.fix_distortion(original_frame)

    # Финально корректируем размер итогового фрейма для устранения лишних участков
    new_frame = new_frame[150:350, 150:850]  # TODO
    new_frame = cv2.resize(new_frame, (1400, 400))  # TODO

    return new_frame


try:
    while True:
        frame = None

        if FPS:
            frame = handle_input()

            if frame is None:
                break

            if NORMALIZE_OUTPUT:
                frame = normalize(frame)

            if CUBE_DETECTION_MODE:
                FPS = sliders.get_setting('FPS')
                frame, edged = detect_cubes(frame)

            if CUBE_DETECTION_MODE and SHOW_CONTOURS:
                handle_output(edged)
            else:
                handle_output(frame)
        else:
            FPS = sliders.get_setting('FPS')

        # Прерывание по нажатию 'q'
        if cv2.waitKey(max(1000 // max(FPS, 1), 1)) & 0xFF == ord('q'):
            break
finally:
    # Освобождаем ресурсы и закрываем окна
    if cap:
        cap.release()

    cv2.destroyAllWindows()
