import telebot

import model_program_3 as md

bot = telebot.TeleBot('6334734199:AAEhk-7XKJysZP6vz7sGAiZuGcAa9aYhb1s')
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = file_info.file_path.split('/')[-1]
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, f'Фотография сохранена. На ней глаза - {md.model_predict(file_name)}')

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.send_message(message.chat.id, 'Ошибка. Пожалуйста, отправьте фотографию')

def other_function(file_path):
    # Здесь можно написать код для работы с фотографией
    pass

bot.polling()