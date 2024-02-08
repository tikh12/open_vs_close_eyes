import cv2,time, camera
import numpy as np

haar_cascade = 'haarcascade_lefteye_2splits.xml'

def predict_vyola_video (file_name):
    start_time = time.time()
    camera = cv2.VideoCapture(file_name)

    # устанавливаем новое разрешение
    width = 1280
    height = 740
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    cascade = cv2.CascadeClassifier(haar_cascade)

    #Формат сохранения
    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))
    out = cv2.VideoWriter('processed_video/video.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (frame_width, frame_height))

    while True:
        ret, frame = camera.read()

        if not ret:
            break

        grayFrame = frame[:,:,:]
        cv2.cvtColor(grayFrame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(grayFrame)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
        out.write(frame)
        cv2.imshow('Frame name', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    end_time = time.time()
    elapsed_time = end_time - start_time
    response = ["processed_video/video.avi", f"Время выполнения: {round(elapsed_time, 2)}"]
    return response


def predict_vyola_photo (file_name):
    start_time = time.time()
    # загрузка классификатора для распознавания глаз
    eye_cascade = cv2.CascadeClassifier(haar_cascade)

    # загрузка изображения
    img = cv2.imread(file_name)

    # преобразование изображения в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # поиск глаз на изображении
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    # отрисовка прямоугольников вокруг глаз
    for (x, y, w, h) in eyes:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # отображение результата
    cv2.imwrite('processed_photo/image.jpg', img)
    end_time = time.time()
    elapsed_time = end_time - start_time
    response = ["processed_photo/image.jpg", f"Время выполнения: {round(elapsed_time, 2)}"]
    return response

