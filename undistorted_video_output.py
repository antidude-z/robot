import cv2
import numpy as np
# RTSP-адрес камеры
rtsp_url = "rtsp://admin:UrFU_ISIT@10.32.9.223:554/Streaming/channels/101"

# Создаем объект для захвата видео
cap = cv2.VideoCapture(rtsp_url)

#camera_matrix = np.array([[804.30675099, 0, 484.55601106],
#                          [0, 820.81782668, 380.41727105],
#                          [0, 0, 1]])
#dist_coefs = np.array([-5.02450741e+00,  2.70083432e+01, -1.17844515e-02, -2.55787550e-03])
#
#size = (3000, 5000)
#sizew = (1676, 846)
#
#newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coefs, (size[0], size[1]), 1, (size[0], size[1]))
#x, y, w, h = roi
#n = 0
## Проверяем успешность подключения
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

        # cap.set(cv2.CAP_PROP_POS_MSEC,200)
        # if ret:
        #     cv2.imwrite(f"./images/frame{n}.png", frame) 
        #     n += 1

        #frame = cv2.undistort(frame, camera_matrix, dist_coefs, None, newcameramtx)
        frame = frame[86:873, 246:1033]

        # Отображаем кадр в окне
        cv2.imshow('IP Camera Stream', frame)

        # Прерывание по нажатию 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Освобождаем ресурсы и закрываем окна
    cap.release()
    cv2.destroyAllWindows()