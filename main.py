import random
import telebot
from telebot import types
import os
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button_image = types.KeyboardButton('Отправить изображение')
    button_audio = types.KeyboardButton('Отправить аудио')
    markup.add(button_image, button_audio)
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=markup)

@bot.message_handler(commands=['repo'])
def send_repo_link(message):
    repo_link = "https://github.com/yourusername/yourrepo"
    bot.send_message(message.chat.id, f"Вот ссылка на репозиторий: {repo_link}")

@bot.message_handler(func=lambda message: message.text == 'Отправить изображение')
def send_image(message):
    photo_path = 'media/img'
    imgs = os.listdir(photo_path)
    rand_img = random.choice(imgs)
    with open(os.path.join(photo_path, rand_img), 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text == 'Отправить аудио')
def send_audio(message):
    audio_path = 'media/audio'
    audios = os.listdir(audio_path)
    rand_audio = random.choice(audios)
    with open(os.path.join(audio_path, rand_audio), 'rb') as audio:
        bot.send_photo(message.chat.id, audio)

bot.polling()
