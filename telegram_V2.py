import telebot
import os
import model_vyola as mv #Метод Виолы Джонса
import predict as p #Классификация изображений
import media_pipe as tmp #Mediapipe

# создание объекта бота
bot = telebot.TeleBot('6334734199:AAEhk-7XKJysZP6vz7sGAiZuGcAa9aYhb1s')

choise_method = 0
choise_attachment = 0

def save_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = f'{file_id}.jpg'
    # получаем путь к текущей директории
    current_dir = os.getcwd()
    # создаем папку для хранения фотографий, если ее нет
    photos_dir = 'telegram_attachment\photo'
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)
    # сохраняем фотографию в папку photos
    photo_path = os.path.join(photos_dir, file_name)
    with open(photo_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    return photo_path


def save_video(message):
    video_id = message.video.file_id
    video_info = bot.get_file(video_id)
    video_path = video_info.file_path
    downloaded_file = bot.download_file(video_path)
    save_path = 'telegram_attachment/video/video.mp4'
    with open(save_path, 'wb') as video_file:
        video_file.write(downloaded_file)
    return save_path

def main_menu(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    classificate_button = telebot.types.InlineKeyboardButton(text='Классификатор изображений',
                                                             callback_data='classificate')
    vyola_button = telebot.types.InlineKeyboardButton(text='Метод Виолы-Джонса', callback_data='vyola')
    media_pipe_button = telebot.types.InlineKeyboardButton(text='MediaPipe', callback_data='media_pipe')
    markup.add(classificate_button, vyola_button, media_pipe_button)

    # отправка сообщения с кнопками пользователю
    bot.send_message(message.chat.id, 'Выберите метод для обработки:', reply_markup=markup)


# функция-обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global choise_method, choise_attachment

    if call.data == 'classificate':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        photo_button = telebot.types.InlineKeyboardButton(text='Загрузить фото', callback_data='classificate_photo')
        markup.add(photo_button)
        bot.send_message(call.message.chat.id, 'Выберите, что вы хотите загрузить:', reply_markup=markup)
    elif call.data == 'classificate_photo':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        choise_method = 1
        choise_attachment = 1
        bot.send_message(call.message.chat.id, 'Загрузите фото с ОДНИМ глазом для распознавания классификатором')

    elif call.data == 'vyola':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        video_button = telebot.types.InlineKeyboardButton(text='Загрузить видео', callback_data='vyola_video')
        photo_button = telebot.types.InlineKeyboardButton(text='Загрузить фото', callback_data='vyola_photo')
        markup.add(video_button,photo_button)
        bot.send_message(call.message.chat.id, 'Выберите, что вы хотите загрузить:', reply_markup=markup)
    elif call.data == 'vyola_video':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        choise_method = 2
        choise_attachment = 2
        bot.send_message(call.message.chat.id, 'Загрузите видео для распознавания методом Виолы-Джонса')
    elif call.data == 'vyola_photo':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        choise_method = 2
        choise_attachment = 1
        bot.send_message(call.message.chat.id, 'Загрузите фото для распознавания методом Виолы-Джонса')

    elif call.data == 'media_pipe':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        video_button = telebot.types.InlineKeyboardButton(text='Загрузить видео', callback_data='media_pipe_video')
        photo_button = telebot.types.InlineKeyboardButton(text='Загрузить фото', callback_data='media_pipe_photo')
        markup.add(video_button, photo_button)
        bot.send_message(call.message.chat.id, 'Выберите, что вы хотите загрузить:', reply_markup=markup)
    elif call.data == 'media_pipe_video':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        choise_method = 3
        choise_attachment = 2
        bot.send_message(call.message.chat.id, 'Загрузите видео для распознавания при помощи MediaPipe')
    elif call.data == 'media_pipe_photo':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        choise_method = 3
        choise_attachment = 1
        bot.send_message(call.message.chat.id, 'Загрузите фото для распознавания при помощи MediaPipe')



# функция-обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def text_handler(message):
    # получение текста сообщения от пользователя
    message_text = message.text
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    # проверка выбора пользователя
    if message_text == 'Классификатор изображений':
        # отправка сообщения с запросом на загрузку фото
        photo_button = telebot.types.KeyboardButton('Загрузить фото')
        markup.add(photo_button)
    elif message_text == 'Метод Виолы-Джонса':
        # отправка сообщения с запросом на загрузку видео
        video_button = telebot.types.KeyboardButton('Загрузить видео')
        photo_button = telebot.types.KeyboardButton('Загрузить фото')
        markup.add(video_button, photo_button)
    elif message_text == 'Media Pipe':
        # отправка сообщения с запросом на загрузку видео
        photo_button = telebot.types.KeyboardButton('Загрузить фото')
        video_button = telebot.types.KeyboardButton('Загрузить видео')
        markup.add(video_button, photo_button)
    else:
        # отправка сообщения об ошибке, если пользователь выбрал что-то другое
        bot.send_message(message.chat.id, 'Пожалуйста, выберите один из вариантов: "Загрузить фото" или "Загрузить видео".')

# функция-обработчик фото и видео
@bot.message_handler(content_types=['photo', 'video'])
def media_handler(message):
    if message.content_type == 'video':
        if (choise_method == 1):
            bot.send_message(message.chat.id, f'Этим методом нельзя обработать видео')
            main_menu(message)
        elif (choise_method == 2):
            bot.send_message(message.chat.id, f'Обработка видео может занять несколько минут')
            response = mv.predict_vyola_video(save_video(message))
            with open(response[0], 'rb') as video_file:
                bot.send_video(message.chat.id, video_file)
            bot.send_message(message.chat.id, f'{response[1]} секунд.')
            main_menu(message)
        elif (choise_method == 3):
            response = tmp.predict_media_pipe_video(save_video(message))
            with open(response[0], 'rb') as video_file:
                bot.send_video(message.chat.id, video_file)
            bot.send_message(message.chat.id, f'{response[1]} секунд.')
            main_menu(message)
        else:
            bot.send_message(message.chat.id, f'Ошибка, нажмите /start')
    else:
        if (choise_method == 1):
            file_name = save_photo(message)
            response = p.predict_model(file_name)
            bot.send_message(message.chat.id, f'Фотография сохранена. На ней глаза - {response[2]}. {response[1]} секунд.')
            main_menu(message)
        elif (choise_method == 2):
            response = mv.predict_vyola_photo(save_photo(message))
            with open(response[0], 'rb') as photo_file:
                bot.send_photo(message.chat.id, photo_file)
            bot.send_message(message.chat.id, f'{response[1]} секунд.')
            main_menu(message)
        elif (choise_method == 3):
            file_name = save_photo(message)
            response = tmp.predict_media_pipe_photo(file_name)
            photo = open(response[0], 'rb')
            bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id, f'{response[1]} секунд.')
            photo.close()
            main_menu(message)
        else:
            bot.send_message(message.chat.id, f'Ошибка, нажмите /start')



# запуск бота
bot.polling()


