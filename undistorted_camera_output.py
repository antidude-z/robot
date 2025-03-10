import cv2
import numpy as np

# RTSP-адрес
rtsp_url = "rtsp://admin:UrFU_ISIT@10.32.9.223:554/Streaming/channels/101"

# Создаем объект для захвата видео
cap = cv2.VideoCapture(rtsp_url)
# cap = cv2.VideoCapture('video/robotCam_tst.avi')

cv2.namedWindow('settings', cv2.WINDOW_NORMAL)
cv2.resizeWindow('settings', 900, 500)


def nothing(n: int) -> None:
    pass


def get_setting(field):
    return cv2.getTrackbarPos(field, 'settings')


def create_setting(name, value, count):
    cv2.createTrackbar(name, 'settings', value, count, nothing)
    cv2.setTrackbarMin(name, 'settings', -count)


create_setting('a1', 528, 1000)
create_setting('a2', 0, 1000)
create_setting('a3', 581, 1000)
create_setting('b1', 0, 1000)
create_setting('b2', 482, 1000)
create_setting('b3', 259, 1000)
create_setting('c1', 0, 1000)
create_setting('c2', 0, 1000)
create_setting('c3', 1, 1000)

create_setting('d1', -289, 1000)
create_setting('d2', 106, 1000)
create_setting('d3', 0, 1000)
create_setting('d4', 0, 1000)
create_setting('d5', -21, 100)


# K = np.array([[279.32886439,   0.,         288.85532134],
#  [  0.,         270.05932082, 182.29417195],
#  [  0.,           0.,           1.        ]])  
# K = np.array([[540.58274027,   0.,         584.44069952],
#  [  0.,         522.21403853, 243.33864001],
#  [  0.,           0.,           1.        ]]) 
# K = np.array([[524.86313844,   0.,         581.53887646],
#  [  0.,         507.44567318, 259.14912353],
#  [  0.,           0.,           1.        ]]) 

# Сама матрица параметров

# D = np.array([-0.31811907,  0.10801802, -0.00077353,  0.00141375, -0.01673607]) 
# D = np.array([-0.33076381,  0.15602231,  0.00237734, -0.00139177, -0.04399833])
# D = np.array([-2.91550736e-01,  1.06626079e-01, -1.89698359e-05,  7.24961162e-04,
#  -2.10373121e-02])

# size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
#         int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
size = (450, 1150)

# newcameramtx, roi = cv2.getOptimalNewCameraMatrix(K, D, (size[0], size[1]), 1, (size[0], size[1]))
# x, y, w, h = roi
# M = cv2.getRotationMatrix2D((size[0]/2,size[1]/2),5,1)


if not cap.isOpened():
    print("Ошибка: Не удалось подключиться к камере")
    exit()

try:
    while True:
        # Считываем кадр из потока
        ret, frame = cap.read()

        frame = frame[700:1150, 700:1850]
        # frame = cv2.resize(frame, [1080, 720])

        K = np.array([[get_setting('a1'), get_setting('a2'), get_setting('a3')],
                      [get_setting('b1'), get_setting('b2'), get_setting('b3')],
                      [get_setting('c1'), get_setting('c2'), get_setting('c3')]])
        D = np.array(
            [get_setting('d1') / 1000, get_setting('d2') / 1000, get_setting('d3') / 1000, get_setting('d4') / 1000,
             get_setting('d5') / 1000])

        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(K, D, (size[0], size[1]), 1, (size[0], size[1]))
        x, y, w, h = roi

        if not ret:
            print("Ошибка: Не удалось получить кадр")
            break

        # frame = frame[y:y+h-50, x+70:x+w-20]
        frame = cv2.undistort(frame, K, D, None, newcameramtx)

        # Отображаем кадр в окне
        cv2.imshow('IP Camera Stream', frame)

        # Прерывание по нажатию 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Освобождаем ресурсы и закрываем окна
    cap.release()
    cv2.destroyAllWindows()
