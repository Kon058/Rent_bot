import sqlite3
import telebot
import os.path
import os
import datetime

token = os.environ.get('TOKEN8')


bot = telebot.TeleBot(token)

text_start = 'ТЦ Березка\n\nТекущий месяц - {month}\n\nОбщее количество арендаторов - {all}\nКоличество оплативших - ' \
             '{pay}\nКоличество не оплативших - {not_pay}'
month = ''
month_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
           'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
def check_base():
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS RENTER(
        renter_id INT PRYMARY KEY,
        name TEXT);
    """)
    cur.execute("""    
        CREATE TABLE IF NOT EXISTS PAYMENTS(
        p_id INT PRYMARY KEY,
        month TEXT,
        stavka INT,
        payment int);
    """)
    conn.commit()

def get_all_rents():
    pass

def get_who_paid():
    pass

def get_who_didnt_pay():
    pass

def get_month():
    d = datetime.datetime.now()
    number_month = int(d.strftime('%m'))
    return month_list[number_month-1]

@bot.message_handler(commands=['start'])
def start_message(message):

    bot.send_message(message.chat.id, text_start.format(month=month, all=20, pay=16, not_pay=4))


check_base()
month = get_month()


bot.polling()


