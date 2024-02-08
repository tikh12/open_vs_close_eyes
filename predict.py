import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from PIL import Image
import numpy as np
from keras.preprocessing import image
import time


def predict_model (image_file_name):
    start_time = time.time()
    #Загрузка изображения из переданного пути с фиксированным разрешением
    img = image.load_img(image_file_name, target_size=(150, 150))

    #Перевод изображения в двумерный массив
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    #Получение двоичной матрицы
    img_array /= 255.

    #Загрузка обученной модели
    model_loaded = keras.models.load_model('Save Models/Model_Version1_epochs15_h5.h5')

    #Подаём изображение на вход модели
    predict = model_loaded.predict(img_array)[0][0]

    end_time = time.time()
    elapsed_time = end_time - start_time

    response = ["processed_photo/image.jpg", f"Время выполнения: {round(elapsed_time, 2)}", ""]

    if abs(predict - 1) < abs(predict):
        response[2] = "Открыты"
    else:
        response[2] = "Закрыты"

    return response





