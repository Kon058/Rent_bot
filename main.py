import sqlite3
import telebot
import os.path
import os


token = os.environ.get('TOKEN8')

#token = '5038240909:AAGK8aF8V3M73EYrpB1K_q6BqIe8T7vqz6k' #668
bot = telebot.TeleBot(token)

text_start = 'ТЦ Березка\n\nКоличество оплативших -\nКоличество не оплативших -'

@bot.message_handler(commands=['start'])
def start_message(message):

    bot.send_message(message.chat.id, text_start)



bot.polling()


