import telebot
from telebot import types

TOKEN = '7529378084:AAFh7cMsZfa68IfnnwTitJsA5s7A0NvaUiA'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("О создателе")
    btn2 = types.KeyboardButton("где ты?")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "да Аникоша?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "О создателе")
def about_me(message):
    bot.send_message(message.chat.id, "Я Бека <3")

@bot.message_handler(func=lambda message: message.text == "где ты?")
def contacts(message):
    bot.send_message(message.chat.id, "в твоем сердце <3")

@bot.message_handler(func=lambda message: message.text not in ["где ты?", "О создателе"])
def echo_all(message):
    bot.send_message(message.chat.id, f"{message.text}?")

bot.polling()
