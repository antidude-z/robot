import cv2
import numpy as np
import glob

files = glob.glob('images/*')
n = 0

# RTSP-адрес
rtsp_url = "rtsp://admin:UrFU_ISIT@10.32.9.223:554/Streaming/channels/101"

# Создаем объект для захвата видео
cap = cv2.VideoCapture(rtsp_url)
# cap = cv2.VideoCapture('video/robotCam_tst_video3.avi')

# fourcc = cv2.VideoWriter.fourcc(*'MP4V')
# out = cv2.VideoWriter('undistorted_video_3.avi', fourcc, 20.0, (1400, 400))

cv2.namedWindow('settings', cv2.WINDOW_NORMAL)
cv2.resizeWindow('settings', 900, 500)


def nothing(n: int) -> None:
    pass


def get_setting(field):
    return cv2.getTrackbarPos(field, 'settings')


def create_setting(name, value, count):
    cv2.createTrackbar(name, 'settings', value, count, nothing)
    cv2.setTrackbarMin(name, 'settings', -count)


create_setting('a1', 529, 1000)
create_setting('a2', 0, 1000)
create_setting('a3', 585, 1000)
create_setting('b1', 4, 1000)
create_setting('b2', 482, 1000)
create_setting('b3', 241, 1000)
create_setting('c1', 0, 1000)
create_setting('c2', 0, 1000)
create_setting('c3', 1, 1000)

create_setting('d1', -292, 1000)
create_setting('d2', 106, 1000)
create_setting('d3', 0, 1000)
create_setting('d4', 0, 1000)
create_setting('d5', -21, 100)

size = (450, 1150)

K = np.array([[get_setting('a1'), get_setting('a2'), get_setting('a3')],
                      [get_setting('b1'), get_setting('b2'), get_setting('b3')],
                      [get_setting('c1'), get_setting('c2'), get_setting('c3')]])
D = np.array(
    [get_setting('d1') / 1000, get_setting('d2') / 1000, get_setting('d3') / 1000, get_setting('d4') / 1000,
        get_setting('d5') / 1000])

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(K, D, (size[0], size[1]), 1, (size[0], size[1]))
x, y, w, h = roi


if not cap.isOpened():
    print("Ошибка: Не удалось подключиться к камере")
    exit()

try:
    while True:
        # Считываем кадр из потока
        # ret, frame = cap.read()

        if n == len(files):
            break

        file = files[n]
        n += 1
        ret, frame = True, cv2.imread(file, cv2.IMREAD_COLOR)

        frame = frame[700:1150, 700:1850]

        # K = np.array([[get_setting('a1'), get_setting('a2'), get_setting('a3')],
        #               [get_setting('b1'), get_setting('b2'), get_setting('b3')],
        #               [get_setting('c1'), get_setting('c2'), get_setting('c3')]])
        # D = np.array(
        #     [get_setting('d1') / 1000, get_setting('d2') / 1000, get_setting('d3') / 1000, get_setting('d4') / 1000,
        #      get_setting('d5') / 1000])

        # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(K, D, (size[0], size[1]), 1, (size[0], size[1]))
        # x, y, w, h = roi

        if not ret:
            print("Ошибка: Не удалось получить кадр")
            break

        frame = cv2.undistort(frame, K, D, None, newcameramtx)

        frame = frame[150:350, 150:850]
        frame = cv2.resize(frame, [1400, 400])

        # out.write(frame)

        # Отображаем кадр в окне
        cv2.imshow('IP Camera Stream', frame)

        cv2.imwrite(f'dataset/img{n}.png', frame)

        # Прерывание по нажатию 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Освобождаем ресурсы и закрываем окна
    cap.release()
    cv2.destroyAllWindows()
