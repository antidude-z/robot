import cv2
import numpy as np

# RTSP-адрес
rtsp_url = "rtsp://admin:UrFU_ISIT@10.32.9.223:554/Streaming/channels/101"

# Создаем объект для захвата видео
cap = cv2.VideoCapture(rtsp_url)

# K = np.array([[627.46226877,   0.,         329.7297745 ],
#  [  0.,         634.75994258, 426.07868156],
#  [  0.,           0.,           1.        ]])
# K = np.array([[606.68017771,   0.,         400.1477127 ],
#  [  0.,         623.53977779, 395.21510025],
#  [  0.,           0.,           1.        ]])  
# K = np.array([[360.03353073,   0.,         411.47450711],
#  [  0.,         350.97754646, 361.57433184],
#  [  0.,           0.,           1.        ]])  
# K = np.array([[1.15875462e+03, 0.00000000e+00, 3.91565460e+02],
#  [0.00000000e+00, 1.12748536e+03, 3.98349397e+02],
#  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])  
# K = np.array([[495.00572315,   0.,         295.37470581],
#  [  0.,         480.46583295, 166.39519288],
#  [  0.,           0.,           1.,        ]])  
K = np.array([[279.32886439,   0.,         288.85532134],
 [  0.,         270.05932082, 182.29417195],
 [  0.,           0.,           1.        ]])  
# Сама матрица параметров

# D = np.array([-1.3100785,  -2.73062637, -0.06422096,  0.14167724,  9.88706302]) 
# D = np.array([-1.49303132,  2.21038416, -0.00336617,  0.00384473, -1.45777788]) 
# D = np.array([-0.50205798,  0.25191986,  0.02121489, -0.01023011, -0.0667614]) 
# D = np.array([-5.48558181e+00,  3.20934950e+01,  6.14130914e-03, -1.16508948e-02, -8.53629154e+01]) 
# D = np.array([-1.08905425,  1.46490697,  0.01505046, -0.01363791, -1.05467567]) 
D = np.array([-0.31811907,  0.10801802, -0.00077353,  0.00141375, -0.01673607]) 
# Коэффициенты искажения (4 элемента) раньше было 5 но я убрал потому что были артефакты

# size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
#         int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
size = (600, 300)

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

        # frame = frame[y:y+h-50, x+70:x+w-20]
        frame = frame[300:600, 350:950]
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