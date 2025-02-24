import cv2
import numpy as np

# RTSP-адрес
rtsp_url = "rtsp://admin:UrFU_ISIT@10.32.9.223:554/Streaming/channels/101"

# Создаем объект для захвата видео
cap = cv2.VideoCapture(rtsp_url)

K = np.array([[804.30675099, 0, 484.55601106],
              [0, 820.81782668, 380.41727105],
              [0, 0, 1]])  
# Сама матрица параметров

D = np.array([-5.02450741e+00,  2.70083432e+01, -1.17844515e-02, -2.55787550e-03]) 
# Коэффициенты искажения (4 элемента) раньше было 5 но я убрал потому что были артефакты

size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(K, D, (size[0], size[1]), 1, (size[0], size[1]))
x, y, w, h = roi
# M = cv2.getRotationMatrix2D((size[0]/2,size[1]/2),5,1)


if not cap.isOpened():
    print("Ошибка: Не удалось подключиться к камере")
    exit()

try:
    while True:
        # Считываем кадр из потока
        ret, frame = cap.read()

        if not ret:
            print("Ошибка: Не удалось получить кадр")
            break

        frame = cv2.undistort(frame, K, D, None, newcameramtx)

        # frame = frame[86:873, 246:1033]
        # frame = frame[y:y+h-50, x+70:x+w-20]

        # Отображаем кадр в окне
        cv2.imshow('IP Camera Stream', frame)

        # Прерывание по нажатию 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Освобождаем ресурсы и закрываем окна
    cap.release()
    cv2.destroyAllWindows()