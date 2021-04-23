import telebot
from bs4 import BeautifulSoup
import requests
import asyncio
import random

from telebot import types

TOKEN = "1702597489:AAH14mb-6C8GZn2QrJZ7hLNDKR0EFjTSeIw"
bot = telebot.TeleBot(TOKEN)

def parsing(target):
    nounsList = []
    verbsList = []
    adjectivesList = []
    predictionsStart = ['Дома тебя ждёт ', 'Сегодня тебе придётся ','Опасайся ',
                        'От test не жди ничего хорошего ',
                        'Не стоит сегодня ',
                        'Беги! Спасайся от ']

    async def getNounsList():
        url = "http://klavogonki.ru/vocs/559"
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        nouns = soup.find_all("td", class_="text")
        for noun in nouns:
            nounsList.append(noun.text)
        return nounsList

    async def getVerbsList():
        url = "https://klavogonki.ru/vocs/557/"
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        verbs = soup.find_all("td", class_="text")
        for verb in verbs:
            verbsList.append(verb.text)
        return verbsList

    async def getAdjectivesList():
        url = "http://klavogonki.ru/vocs/558"
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        adjectives = soup.find_all("td", class_="text", limit=100)
        for adjective in adjectives:
            adjectivesList.append(adjective.text)
        return adjectivesList

    async def main():
        main_loop.create_task(getNounsList())
        main_loop.create_task(getVerbsList())
        main_loop.create_task(getAdjectivesList())

    main_loop = asyncio.new_event_loop()
    main_loop.run_until_complete(main())

    if target == "sentence":

        sentence = adjectivesList[random.randint(0, 100)].title() + \
                   ' ' + nounsList[random.randint(0, 100)] + \
                   ' ' + verbsList[random.randint(0, 100)] + \
                   ' ' + nounsList[random.randint(0, 100)]

        return sentence

    elif target == "prediction":
        i = random.randint(0, 5)
        if i == 3:
            sentence = predictionsStart[i].replace('test', nounsList[random.randint(0, 100)])
        else:
            sentence = predictionsStart[i] + nounsList[random.randint(0, 100)]

        return sentence


@bot.message_handler(commands=['start'])
def command_start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    prediction = types.KeyboardButton(text="Предсказание")
    sentence = types.KeyboardButton(text="Предложение")
    keyboard.add(prediction, sentence)
    bot.reply_to(message, "Выбрай", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def whatWouldYouDo(message):
    if message.text == "Сделай предложение":
        bot.send_message(message.from_user.id, parsing("sentence"))
    if message.text == "Предсказание":
        bot.send_message(message.from_user.id, parsing("prediction"))

bot.polling()