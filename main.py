import sqlite3
import telebot
from telebot import types
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

stat_menu = {
    'who_paid': 'Оплаченная аренда',
    'who_didnt_pay': 'Не оплаченная аренда',
    'all': 'Полный список'
}

who_paid_menu = {
    'cansel': 'Убрать арендную плату',
    'change_month': 'Выбрать другой месяц',
    'stat_menu': 'Назад'
}
who_didnt_pay_menu = {
    'who_paid': 'Внести арендную плату',
    'change_month': 'Выбрать другой месяц',
    'stat_menu': 'Назад'
}
all_list_renter = {
    'add_renter': 'Добавить арендатора',
    'del_renter': 'Удалить арендатора',
    'change': 'Изменить данные',
    'stat_menu': 'Назад'
}
def check_base():
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS RENTER(
        r_id INT PRYMARY KEY,
        name TEXT);
    """)
    cur.execute("""    
        CREATE TABLE IF NOT EXISTS PAYMENTS(
        p_id INT PRYMARY KEY,
        month TEXT,
        stavka INT,
        payment int,
        renter_id INT,
        FOREIGN KEY (renter_id) REFERENCES RENTER (r_id));
    """)
    conn.commit()

def get_all_rents():
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    query = """SELECT name FROM RENTER;"""
    cur.execute(query)
    conn.commit()
    return cur.fetchall()

def get_who_paid():
    pass

def get_who_didnt_pay():
    pass

def get_month():
    d = datetime.datetime.now()
    number_month = int(d.strftime('%m'))
    return month_list[number_month-1]

def mani_menu(data, dict, text):
    mainmenu = types.InlineKeyboardMarkup()
    for i in dict:
        bt = types.InlineKeyboardButton(text=dict[i], callback_data=i)
        mainmenu.row(bt)
    bot.send_message(data, text, reply_markup=mainmenu, disable_web_page_preview=True)

@bot.message_handler(commands=['start'])
def start_message(message):
    mani_menu(message.chat.id, stat_menu, text_start.format(month=month, all=len(get_all_rents()), pay=16, not_pay=4))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global location_in_menu
    if call.data == 'main':
        pass



check_base()
month = get_month()

bot.polling()


