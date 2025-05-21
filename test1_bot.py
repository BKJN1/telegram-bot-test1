import telebot
from telebot import types
import requests

TOKEN = '7529378084:AAFh7cMsZfa68IfnnwTitJsA5s7A0NvaUiA'
WEATHER_API_KEY = 'c1244cd715f42ceee9f01cc84e1981fd'
bot = telebot.TeleBot(TOKEN)

def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Kokshetau&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        return f"🌤 Сейчас в Кокшетау: {temp}°C, ощущается как {feels_like}°C.\nОписание: {description}"
    else:
        return "⚠ Не удалось получить данные о погоде."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("О создателе")
    btn2 = types.KeyboardButton("где ты?")
    btn3 = types.KeyboardButton("Погода в Кокшетау")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "да Аникоша?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "О создателе")
def about_me(message):
    bot.send_message(message.chat.id, "Я Бека <3")

@bot.message_handler(func=lambda message: message.text == "где ты?")
def contacts(message):
    bot.send_message(message.chat.id, "в твоем сердце <3")

@bot.message_handler(func=lambda message: message.text == "Погода в Кокшетау")
def weather_kokshetau(message):
    weather_info = get_weather()
    bot.send_message(message.chat.id, weather_info)

@bot.message_handler(func=lambda message: message.text not in ["где ты?", "О создателе", "Погода в Кокшетау"])
def echo_all(message):
    bot.send_message(message.chat.id, f"{message.text}?")

bot.polling()
