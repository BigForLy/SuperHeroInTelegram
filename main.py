import telebot
from const import TOKEN, ADMIN
from log_in_file import log_in_file
from heroes_manager import HeroManager, SendManager

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: log_in_file(message.chat.username + ': start/help'),
                     commands=['start', 'help'])
def c_send_welcome(message):
    bot.send_message(message.chat.id, 'Enter the name of the SuperHero')


@bot.message_handler(commands=['log'])
def c_log(message):
    if message.chat.id == ADMIN:
        try:
            log_file = open('log.txt', 'rb')
            bot.send_document(message.chat.id, log_file)
            log_file.close()
        except Exception as ex:
            bot.send_message(message.chat.id, str(ex))


@bot.message_handler(func=lambda message: log_in_file(message.chat.username + ': ' + message.text),
                     content_types=['text'])
def c_text(message):
    bot.send_message(message.chat.id, 'Search started. Please Wait.')
    heroes = HeroManager(message.text)
    if heroes.error is not None:
        bot.send_message(message.chat.id, heroes.error)
    elif heroes.hero_selected:
        SendManager(heroes, bot, message.chat.id)
    del heroes


if __name__ == '__main__':
    bot.polling()
