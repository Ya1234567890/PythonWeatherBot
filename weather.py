import telebot
from telebot import types
import requests
import wikipediaapi
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN, API_KEY = 'TOKEN', 'API_KEY'
bot = telebot.TeleBot(TOKEN)


def get_weather(city, API_KEY):
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric')
        data = response.json()
        city = data['name']
        temp = data['main']['temp']
        pres = data['main']['pressure']
        wind_speed = data['wind']['speed']
        hum = data['main']['humidity']
        wiki_wiki = wikipediaapi.Wikipedia('ru')
        result = wiki_wiki.page(city)
        res = result.summary
        if len(res) > 0:
            s = f'\n \n \n А теперь немного интересного о городе: \n {res}'
        else:
            s = ''
        return f' Погода в {city}:\n температура = {temp} С\n давление = {pres} мм рт. ст.\n скорость ветра = {wind_speed} м/с \n влажность = {hum} % {s}'
    except:
        return 'Похоже, вы неправильно указали название города! :('


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Здравствуйте! Я бот-синоптик. Отправьте мне название города, и я пришлю вам погоду в нём. Введите команду "/help" для получения более подробной информации о боте')


@bot.message_handler(commands=['help'])
def buttons(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('источник прогнозов погоды'), types.KeyboardButton('о проекте'))
    bot.send_message(message.chat.id, 'Что Вас интересует?', reply_markup=markup)


@bot.message_handler(regexp='о проекте')
def project_inf(message):
    bot.send_message(message.chat.id,
                     'Здравствуйте! Этот бот является проектом студента курса "Python Pro". Бот может помочь Вам получить сведения о погоде в любом выбранном вами городе, а также немного рассказать о нём')


@bot.message_handler(regexp='источник прогнозов погоды')
def web(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Сайт с погодой', url='https://openweathermap.org'))
    bot.send_message(message.chat.id, 'Посетить сайт, откуда берётся информация о погоде', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_weather(message):
    bot.send_message(message.chat.id, get_weather(message.text, API_KEY))


bot.infinity_polling()
