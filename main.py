import telebot
from telebot import types
import os
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
CATS_API_KEY = os.getenv("CATS_API_KEY")


def get_random_cat_image():
    url = "https://api.thecatapi.com/v1/images/search"
    headers = {
        "x-api-key": CATS_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data[0]["url"]
    else:
        raise Exception(f"Ошибка при обращении к The Cat API: {response.status_code}")

import requests
import random

def get_random_sound():
    url = "https://www.xeno-canto.org/api/2/recordings?query=cat"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Ошибка API xeno-canto: {response.status_code}")
    
    data = response.json()
    if not data.get("recordings"):
        raise Exception("Нет доступных записей.")
    
    # Случайный выбор записи
    random_recording = random.choice(data["recordings"])
    return random_recording["file"]  # Ссылка на аудиофайл



@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    button_image = types.KeyboardButton('Отправить изображение')
    button_audio = types.KeyboardButton('Отправить аудио')
    markup.add(button_image, button_audio)
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=markup)

@bot.message_handler(commands=['repo'])
def send_repo_link(message):
    repo_link = "https://github.com/andr3yb/simple_bot"
    bot.send_message(message.chat.id, f"Ссылка на репозиторий: {repo_link}")

@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id, "Бот остановлен. Чтобы запустить снова, отправьте /start.")
    bot.send_message(message.chat.id, "Клавиатура скрыта.", reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: message.text == 'Отправить изображение')
def send_image(message):
    try:
        image_url = get_random_cat_image()
        bot.send_photo(message.chat.id, image_url)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при получении изображения: {e}")

@bot.message_handler(func=lambda message: message.text == 'Отправить аудио')
def send_random_audio(message):
    try:
        audio_url = get_random_sound()
        bot.send_message(message.chat.id, f"Звук: {audio_url}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")


bot.set_my_commands([
    telebot.types.BotCommand("start", "Запустить бота"),
    telebot.types.BotCommand("stop", "Остановить бота"),
    telebot.types.BotCommand("repo", "Ссылка на репозиторий"),
])



bot.polling()
