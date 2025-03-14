import cv2
import glob

from config import *
from src.camera_tools import undistort, sliders
from src.camera_tools.detector import DetectableObject
from src.camera_tools.input_source import InputSource

LOWER_B_Y, UPPER_B_Y = NORMALIZED_DIMENSIONS[0][0], NORMALIZED_DIMENSIONS[0][1]
LOWER_B_X, UPPER_B_X = NORMALIZED_DIMENSIONS[1][0], NORMALIZED_DIMENSIONS[1][1]
NORMALIZED_RESIZE = ((UPPER_B_Y - LOWER_B_Y) * NORMALIZED_RESIZE_RATE,
                     (UPPER_B_X - LOWER_B_X) * NORMALIZED_RESIZE_RATE)


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
        size = NORMALIZED_RESIZE[::-1]
    else:
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    out = cv2.VideoWriter(VIDEO_OUTPUT_PATH, fourcc, 20.0, size)

if IMAGE_FILE_OUTPUT:
    def gen_next_number():
        n = 0
        while True:
            n += 1
            yield n


    gen = gen_next_number()

if ADJUST_COEFFS_REALTIME:
    coeffs_win = sliders.Window('coeffs')

    symbols = ['a', 'b', 'c']

    for i in range(4):
        if i < 3:
            for k in range(3):
                coeffs_win.create_setting(f'{symbols[i]}{k + 1}', DEFAULT_K[i][k], K_RANGE)
        else:
            for k in range(5):
                coeffs_win.create_setting(f'd{k + 1}', DEFAULT_D[k], D_RANGE)
else:
    undistort.make_matrix(DEFAULT_K, list(map(lambda x: x / 1000, DEFAULT_D)), FISHEYE_DIMENSIONS)

if DETECTION_DEMO:
    det_sliders_win = sliders.Window('detect')
    det_sliders_win.create_multiple_settings([('FPS', 40, 400, 0),
                                              ('blue_lower', 0, 255, 0), ('green_lower', 50, 255, 0),
                                              ('red_lower', 0, 255, 0), ('blue_upper', 75, 255, 0),
                                              ('green_upper', 255, 255, 0), ('red_upper', 50, 255, 0),
                                              ('blur', 3, 30, 0), ('ksize', 30, 50, 0), ('area', 1000, 10000, 0),
                                              ('morph', 0, 0, 0)])


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
    if ADJUST_COEFFS_REALTIME:
        k = [coeffs_win.gather(f'{s}1', f'{s}2', f'{s}3') for s in ('a', 'b', 'c')]
        d = list(map(lambda x: x / 1000, coeffs_win.gather('d1', 'd2', 'd3', 'd4', 'd5')))

        undistort.make_matrix(k, d, FISHEYE_DIMENSIONS)

    new_frame = undistort.fix_distortion(original_frame)

    # Финально корректируем размер итогового фрейма для устранения лишних участков
    new_frame = new_frame[LOWER_B_Y: UPPER_B_Y, LOWER_B_X: UPPER_B_X]
    new_frame = cv2.resize(new_frame, NORMALIZED_RESIZE[::-1])

    return new_frame


try:
    while True:
        frame = None

        if DETECTION_DEMO:
            FPS = det_sliders_win.get_setting('FPS')

            blur_val, ksize = det_sliders_win.gather('blur', 'ksize')
            lowerb = det_sliders_win.gather('blue_lower', 'green_lower', 'red_lower')
            upperb = det_sliders_win.gather('blue_upper', 'green_upper', 'red_upper')
            area = det_sliders_win.get_setting('area')
            morph = [cv2.MORPH_RECT][det_sliders_win.get_setting('morph')]  # TODO

            demo_obj = DetectableObject(blur_val, lowerb, upperb, ksize, area, morph)

        if FPS:
            frame = handle_input()

            if frame is None:
                break

            if NORMALIZE_OUTPUT:
                frame = normalize(frame)

            if DETECTION_DEMO:
                frame = demo_obj.proceed(frame, SHOW_CONTOURS)
            elif DETECTION_MODE:
                for name, obj in OBJECTS.items():
                    frame = obj.proceed(frame, SHOW_CONTOURS)

            handle_output(frame)

        # Прерывание по нажатию 'q'
        if cv2.waitKey(max(1000 // max(FPS, 1), 1)) & 0xFF == ord('q'):
            break
finally:
    # Освобождаем ресурсы и закрываем окна
    if cap:
        cap.release()

    cv2.destroyAllWindows()
