import cv2

# RTSP-адрес камеры
rtsp_url = "rtsp://admin:UrFU_ISIT@10.32.9.223:554/Streaming/channels/101"

# Создаем объект для захвата видео
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Ошибка: Не удалось подключиться к камере")
    exit()

n = 0

try:
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Ошибка: Не удалось получить кадр")
            break

        frame = frame[300:600, 350:950]

        cap.set(cv2.CAP_PROP_POS_MSEC, 200)
        cv2.imwrite(f'./images/frame{n}.png', frame)
        n += 1

        # Отображаем кадр в окне
        cv2.imshow('IP Camera Stream', frame)

        # Прерывание по нажатию 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Освобождаем ресурсы и закрываем окна
    cap.release()
    cv2.destroyAllWindows()
