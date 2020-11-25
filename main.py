from io import BytesIO
from telegram import Update
import telebot;
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import Filters
import requests
from exif_reader import get_exif_data, get_location

bot = Updater('здесь токен')

# ответ на команду start
def hello_message(update: Update, context: CallbackContext):
    user_first_name = update.message.from_user.first_name

    update.message.reply_text(f"Привет, {user_first_name}")


# ответ на сообщения
def answer_message(update: Update, context: CallbackContext):
    if update.message.text == "Привет" or update.message.text == "привет":
        update.message.reply_text("Привет, чем я могу тебе помочь?")
    elif update.message.text == "/help":
        update.message.reply_text("Напиши привет")
    else:
        update.message.reply_text("Я тебя не понимаю. Напиши /help.")


# обработчик фотографий
def reply_to_photo(update: Update, context: CallbackContext):
    document = update.message['document']
    file_id = document['file_id']
    mime_type = document['mime_type']

    # проверка формата полученного файла
    if not mime_type.startswith('image'):
        update.message.reply_text('Я принимаю только файлы с картинками')

    file_info_link = (f'https://api.telegram.org/bot1434968021:AAGyvLYKaYoBUFSqZYjkTphGW0lhRAiwOyE'
                      f'/getFile?file_id={file_id}')
    file_path = requests.get(file_info_link).json()['result']['file_path']
    file_link = f'https://api.telegram.org/file/bot1434968021:AAGyvLYKaYoBUFSqZYjkTphGW0lhRAiwOyE/{file_path}'
    file = requests.get(file_link).content
    file_data = BytesIO(file)
    exif_data = get_exif_data(file_data)
    lat, lon = get_location(exif_data)

    update.message.reply_text(f"Координаты: {lat}, {lon}")



def main():
    # Разбор входящих сообщений
    dp = bot.dispatcher
    dp.add_handler(CommandHandler("start", hello_message))
    dp.add_handler(MessageHandler(Filters.document, reply_to_photo))
    dp.add_handler(MessageHandler(Filters.text, answer_message))
    bot.start_polling()
    bot.idle()

if __name__ == '__main__':
    main()
