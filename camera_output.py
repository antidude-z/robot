import cv2
import numpy as np
# RTSP-адрес камеры
rtsp_url = "rtsp://admin:UrFU_ISIT@10.32.9.223:554/Streaming/channels/101"

# Создаем объект для захвата видео
cap = cv2.VideoCapture(rtsp_url)

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