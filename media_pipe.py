import cv2
import mediapipe as mp
import time


def eye_aspect_ratio(face_landmarks, eye_indices):
    # вычисление расстояний между верхней и нижней частями глаза
    A = face_landmarks.landmark[eye_indices[1]].y - face_landmarks.landmark[eye_indices[5]].y
    B = face_landmarks.landmark[eye_indices[2]].y - face_landmarks.landmark[eye_indices[4]].y

    # вычисление расстояния между крайними точками глаза по горизонтали
    C = face_landmarks.landmark[eye_indices[0]].x - face_landmarks.landmark[eye_indices[3]].x

    # вычисление отношения высоты верхней и нижней частей глаза к расстоянию между крайними точками глаза по горизонтали
    ear = (A + B) / (2 * C)

    return ear



def predict_media_pipe_photo (file_name):
    start_time = time.time()

    # Инициализация объекта класса mp для обнаружения лица и глаз
    mp_face_detection = mp.solutions.face_detection
    mp_face_mesh = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils

    # Загрузка изображения
    image = cv2.imread(file_name)

    # Преобразование изображения в RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Обнаружение лица на изображении
    with mp_face_detection.FaceDetection(model_selection=1) as face_detection:
        results = face_detection.process(image)
        if results.detections:
            for detection in results.detections:
                # Обнаружение глаз на изображении
                with mp_face_mesh.FaceMesh() as face_mesh:
                    landmarks = face_mesh.process(image)
                    left_eye_landmarks = [landmarks.multi_face_landmarks[0].landmark[i] for i in
                                          [362, 385, 387, 263, 373, 380]]
                    right_eye_landmarks = [landmarks.multi_face_landmarks[0].landmark[i] for i in
                                           [33, 160, 158, 133, 153, 144]]

                    # Вычисление отношения высоты закрытых глаз к открытым глазам
                    left_eye_height_ratio = (left_eye_landmarks[4].y - left_eye_landmarks[1].y) / (
                            left_eye_landmarks[3].y - left_eye_landmarks[2].y)
                    right_eye_height_ratio = (right_eye_landmarks[4].y - right_eye_landmarks[1].y) / (
                            right_eye_landmarks[3].y - right_eye_landmarks[2].y)

                    # Определение, закрыты ли глаза
                    if (left_eye_height_ratio < 0.2 and right_eye_height_ratio < 0.2):
                        print(f"Оба глаза закрыты. left - {left_eye_height_ratio}, right - {right_eye_height_ratio}")
                    elif (left_eye_height_ratio >= 0.2 and right_eye_height_ratio < 0.2):
                        print(
                            f"Левый глаз открыт, правый глаз закрыт. left - {left_eye_height_ratio}, right - {right_eye_height_ratio}")
                    elif (left_eye_height_ratio < 0.2 and right_eye_height_ratio >= 0.2):
                        print(
                            f"Левый глаз закрыт, правый глаз открыт. left - {left_eye_height_ratio}, right - {right_eye_height_ratio}")
                    else:
                        print(f"Оба глаза открыты. left - {left_eye_height_ratio}, right - {right_eye_height_ratio}")

                # Отрисовка прямоугольника вокруг лица и точек, обозначающих глаза
                mp_drawing.draw_detection(image, detection)
                mp_drawing.draw_landmarks(image, landmarks.multi_face_landmarks[0], mp_face_mesh.FACEMESH_CONTOURS,
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1),
                                          mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1))

    # Вывод изображения с отрисованными прямоугольниками и точками
    cv2.imwrite('processed_photo/image.jpg', image)
    # cv2.imshow("Image", image)
    cv2.waitKey(0)

    # video.release()
    cv2.destroyAllWindows()

    end_time = time.time()
    elapsed_time = end_time - start_time
    response = ["processed_photo/image.jpg", f"Время выполнения: {round(elapsed_time, 2)}"]
    return response


def predict_media_pipe_video(file_name):
    start_time = time.time()
    # загрузка модели для обнаружения ключевых точек лица и глаз
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh()
    mp_drawing = mp.solutions.drawing_utils

    # загрузка видео
    cap = cv2.VideoCapture(file_name)

    # устанавливаем новое разрешение
    width = 1280
    height = 740
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    # Формат сохранения
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter('processed_video/video.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (frame_width, frame_height))


    while True:
        # чтение кадра из видео
        ret, frame = cap.read()
        if not ret:
            break

        # преобразование изображения в RGB и обнаружение ключевых точек лица и глаз
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        # отрисовка ключевых точек на изображении
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS, mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1), mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1))

                # обнаружение открытых и закрытых глаз
                left_eye_ratio = eye_aspect_ratio(face_landmarks, [362, 385, 387, 263, 373, 380])
                right_eye_ratio = eye_aspect_ratio(face_landmarks, [33, 160, 158, 133, 153, 144])

                # вывод состояния глаз на изображение
                if left_eye_ratio < 0.11 and right_eye_ratio < 0.11:
                    cv2.putText(frame, f"Eyes closed.", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, f"Left EAR = {left_eye_ratio}, Right EAR = {right_eye_ratio}", (0, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Eyes open", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f"Left EAR = {left_eye_ratio}, Right EAR = {right_eye_ratio}", (0, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # отображение результата
        out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    end_time = time.time()
    elapsed_time = end_time - start_time
    response = ["processed_video/video.avi", f"Время выполнения: {round(elapsed_time, 2)}"]
    return response


