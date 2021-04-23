import telebot
from bs4 import BeautifulSoup
import requests
import asyncio
import random
import pymorphy2

TOKEN = "1702597489:AAH14mb-6C8GZn2QrJZ7hLNDKR0EFjTSeIw"
bot = telebot.TeleBot(TOKEN)

def parsing():
    nounsList = []
    verbsList = []
    adjectivesList = []
    morph = pymorphy2.MorphAnalyzer()

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

    sentence = adjectivesList[random.randint(0, 100)].title() +\
               ' ' + nounsList[random.randint(0, 100)] +\
               ' ' + verbsList[random.randint(0, 100)] + \
               ' ' + nounsList[random.randint(0, 100)]

    return sentence

@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, "Hello")

@bot.message_handler(content_types=['text'])
def whatWouldYouDo(message):
    if message.text == "Сделай предложение":
        bot.send_message(message.from_user.id, parsing())

bot.polling()