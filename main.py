#Создание и обучение модели
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.src.layers import Conv2D, Activation, MaxPooling2D, Flatten, Dense, Dropout
from keras.src.preprocessing.image import ImageDataGenerator
import scipy.integrate as integrate
# import visualkeras
# from PIL import ImageFont
# import pydot
# import graphviz




# Каталог с изображениями глаз для обучения
train_dir = 'train'
# Каталог с изображениями глаз  для проверки
val_dir = 'val'
# Каталог с изображениями глаз для тестирования
test_dir = 'test'
# Размеры изображения
img_width, img_height = 150, 150
# Размерность тензора на основе изображения для входных данных в нейронную сеть
input_shape = (img_width, img_height, 3)
# Количество эпох
epochs = 8
# Размер мини-выборки
batch_size = 16
# Количество изображений для обучения (Открытые глаза - закрытые)
nb_train_samples = 32264 + 32961
# Количество изображений для проверки (Открытые глаза - закрытые)
nb_validation_samples = 2096 + 4097
# Количество изображений для тестирования (Открытые глаза - закрытые)
nb_test_samples = 6020 + 4237


# Архитектура сети
#
# Слой свертки, размер ядра 3х3, количество карт признаков - 32 шт., функция активации ReLU.
# Слой подвыборки, выбор максимального значения из квадрата 2х2
# Слой свертки, размер ядра 3х3, количество карт признаков - 32 шт., функция активации ReLU.
# Слой подвыборки, выбор максимального значения из квадрата 2х2
# Слой свертки, размер ядра 3х3, количество карт признаков - 64 шт., функция активации ReLU.
# Слой подвыборки, выбор максимального значения из квадрата 2х2
# Слой преобразования из двумерного в одномерное представление
# Полносвязный слой, 64 нейрона, функция активации ReLU.
# Слой Dropout.
# Выходной слой, 1 нейрон, функция активации sigmoid
# Слои с 1 по 6 используются для выделения важных признаков в изображении, а слои с 7 по 10 - для классификации.

model = keras.Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

#Компилируем модель
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])
#
#
# # Генератор изображений создается на основе класса ImageDataGenerator. Генератор делит значения всех пикселов изображения на 255.
datagen = ImageDataGenerator(rescale=1. / 255)
#
# # Генератор данных для обучения на основе изображений из каталога
train_generator = datagen.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')
#
# # Генератор данных для проверки на основе изображений из каталога
val_generator = datagen.flow_from_directory(
    val_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')
# #
# # Генератор данных для тестирования на основе изображений из каталога
test_generator = datagen.flow_from_directory(
    test_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')




# Получение истории обучения
# history = model.fit(x_train, y_train, epochs=10, validation_data=(x_val, y_val))
# train_acc = history.history['accuracy']
# val_acc = history.history['val_accuracy']
# train_loss = history.history['loss']
# val_loss = history.history['val_loss']

#
# # Обучаем модель с использованием генераторов
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=val_generator,
    validation_steps=nb_validation_samples // batch_size)

# #Сохраняем модель
model.save('Save Models/Model_Version1_epochs7_with_metrics_h5.h5')

# # Оцениваем качество работы сети
# Загрузка обученной модели
model_loaded = keras.models.load_model('Save Models/Model_Version1_epochs7_with_metrics_h5.h5')

# #прогоняем тестовую выборку для проверки точности
scores = model_loaded.evaluate_generator(test_generator, nb_test_samples // batch_size)

accuracy = scores[1]
precision_val = scores[2]
recall_val = scores[3]
f1_score = (2 * precision_val * recall_val) / (precision_val + recall_val)

print("Точность на тестовых данных: %.2f%%" % (accuracy*100))
print("Доля верно предсказанных положительных классов на тестовых данных: %.2f%%" % (precision_val*100))
print("Полнота алгоритма на тестовых данных: %.2f%%" % (recall_val*100))
print("Гармоническое среднее точности и полноты алгоритма: %.2f%%" % (f1_score*100))



# import visualkeras
# from PIL import ImageFont
# visualkeras.layered_view(model_loaded, to_file='model.png', scale_xy=2)
#
#
# tf.keras.utils.plot_model(
# model_loaded,
# to_file="model_schem.png",
# show_shapes=True,
# show_dtype=False,
# show_layer_names=True,
# rankdir="TB",
# expand_nested=True,
# dpi=96,
# layer_range=None,
# show_layer_activations=True,
# )

