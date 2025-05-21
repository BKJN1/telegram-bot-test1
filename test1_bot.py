import telebot
from telebot import types
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Храни токен в .env
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(TOKEN)

user_states = {}  # user_id -> state ('menu' или 'chat_with_ai')


def query_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",  # можно указать любой сайт
        "X-Title": "TelegramBot"
    }
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            print("OpenRouter Error:", response.status_code, response.text)
            return "Извини, сейчас не могу ответить."
    except Exception as e:
        print("Ошибка OpenRouter:", e)
        return "Произошла ошибка при обращении к AI."


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


def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("О создателе")
    btn2 = types.KeyboardButton("где ты?")
    btn3 = types.KeyboardButton("Погода в Кокшетау")
    btn4 = types.KeyboardButton("Поболтать с AI")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(chat_id, "да Аникоша?", reply_markup=markup)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_states[message.from_user.id] = 'menu'
    send_main_menu(message.chat.id)


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    user_id = message.from_user.id
    text = message.text
    state = user_states.get(user_id, 'menu')

    if state == 'menu':
        if text == "О создателе":
            bot.send_message(message.chat.id, "твой принц же 🙄❤️")
        elif text == "где ты?":
            bot.send_message(message.chat.id, "в твоем сердце <3")
        elif text == "Погода в Кокшетау":
            weather_info = get_weather()
            bot.send_message(message.chat.id, weather_info)
        elif text == "Поболтать с AI":
            user_states[user_id] = 'chat_with_ai'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_exit = types.KeyboardButton("Выйти из чата с AI")
            markup.add(btn_exit)
            bot.send_message(message.chat.id, "Привет! Пиши что угодно, я — доверенное лицо mr. Bekezhan. \nЧтобы выйти, нажми кнопку ниже.", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"{text}?")
    elif state == 'chat_with_ai':
        if text == "Выйти из чата с AI":
            user_states[user_id] = 'menu'
            send_main_menu(message.chat.id)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            answer = query_openrouter(text)
            bot.send_message(message.chat.id, answer)


print("🤖 Бот запущен")
bot.polling()
