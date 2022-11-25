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
month_list = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
           'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
location_menu = ''
input_name = ''
input_stavka = 0
list_delete = []
month_start = ''
stat_menu = {
    'who_paid': 'Оплаченная аренда',
    'who_didnt_pay': 'Не оплаченная аренда',
    'change_month': 'Выбрать другой месяц',
    'all': 'Полный список'
}
who_paid_menu = {
    'cansel': 'Убрать арендную плату',
    'stat_menu': 'Назад'
}
who_didnt_pay_menu = {
    'set_who_paid': 'Внести арендную плату',
    'stat_menu': 'Назад'
}
all_menu = {
    'add_renter': 'Добавить арендатора',
    'del_renter': 'Удалить арендатора',
    'change': 'Изменить данные',
    'stat_menu': 'Назад'
}
def check_base():
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS RENTER(
        r_id integer primary key AUTOINCREMENT,
        name TEXT,
        stavka INT,
        month_start text);
    """)
    cur.execute("""    
        CREATE TABLE IF NOT EXISTS PAYMENTS(
        p_id integer primary key AUTOINCREMENT,
        month TEXT,
        payment int,
        renter_id INT,
        FOREIGN KEY (renter_id) REFERENCES RENTER (r_id) ON DELETE CASCADE);
    """)
    conn.commit()

def get_all_rents():
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    query = """SELECT * FROM RENTER;"""
    cur.execute(query)
    conn.commit()
    return cur.fetchall()

def get_who_paid(month):
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    query = """SELECT * FROM PAYMENTS INNER JOIN RENTER ON (PAYMENTS.'renter_id'=RENTER.'r_id') WHERE month = :month;"""
    cur.execute(query, {'month': month})
    conn.commit()
    return cur.fetchall()

def get_who_didnt_pay(month):
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    query = """SELECT * FROM PAYMENTS INNER JOIN RENTER ON (PAYMENTS.'renter_id'=RENTER.'r_id') WHERE month != :month;"""
    cur.execute(query, {'month': month})
    conn.commit()
    return cur.fetchall()


def add_rent(name, stavka, month_start):
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    query = """INSERT INTO RENTER (name, stavka, month_start) VALUES(:name_renter, :stavka_renter, :month_start);"""
    cur.execute(query, {'name_renter': name, 'stavka_renter': stavka, 'month_start': month_start})
    conn.commit()


def del_rent(id):
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    query = """DELETE FROM RENTER WHERE r_id = :id;"""
    cur.execute(query, {'id' : id})
    conn.commit()

def get_month():
    d = datetime.datetime.now()
    number_month = int(d.strftime('%m'))
    return month_list[number_month-1]

def mani_menu(data, dict, text):
    mainmenu = types.InlineKeyboardMarkup()
    for i in dict:
        bt = types.InlineKeyboardButton(text=dict[i], callback_data=i)
        mainmenu.row(bt)
    bot.send_message(data, text, reply_markup=mainmenu)
def print_full_list(calldata):
    text_out = 'Полный список арендаторов\n\n'
    full_list = get_all_rents()
    for i in full_list:
        text_out = text_out + i[1] + ' - ' + str(i[2]) + '\n'
    mani_menu(calldata, all_menu, text_out)

def change_month(calldata, text_out):
    mainmenu = types.InlineKeyboardMarkup()
    for i in month_list:
        bt = types.InlineKeyboardButton(text=i, callback_data=i)
        mainmenu.row(bt)
    bt_back = types.InlineKeyboardButton(text='Назад', callback_data='stat_menu')
    mainmenu.row(bt_back)
    bot.send_message(calldata, text_out, reply_markup=mainmenu)

def full_list_renter(calldata, text_for_out, options, back, stavka=None):
    k = []
    list_delete = get_all_rents()
    text_out = 'Полный список арендаторов\n\n'
    mainmenu = types.InlineKeyboardMarkup()
    for count, i in enumerate(list_delete):
        if stavka:
            text_out = text_out + str(count) + '. ' + i[1] + ' - ' + str(i[2]) + '\n'
        else:
            text_out = text_out + str(count) + '. ' + i[1] + '\n'
        k.append(types.InlineKeyboardButton(text=str(count), callback_data=options + str(i[0])))
        if len(k) == 5 or count == (len(list_delete) - 1):
            mainmenu.row(*k)
            k.clear()
    bt_back = types.InlineKeyboardButton(text='Назад', callback_data=back)
    mainmenu.row(bt_back)
    bot.send_message(calldata, text_out)
    bot.send_message(calldata, text_for_out, reply_markup=mainmenu)

def add_contribute(id, pay):
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    query = """INSERT INTO PAYMENTS (month, payment, renter_id) VALUES(:month, :pay, :id);"""
    cur.execute(query, {'month': month, 'pay': pay, 'id': id})
    conn.commit()

@bot.message_handler(commands=['start'])
def start_message(message):
    mani_menu(message.chat.id, stat_menu, text_start.format(month=month, all=len(get_all_rents()), pay=len(get_who_paid(month)), not_pay=99))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global month, location_menu, list_delete
    if call.data == 'who_paid':
        text_out = 'Оплатившие аренду'
        mani_menu(call.message.chat.id, who_paid_menu, text_out)
    elif call.data == 'who_didnt_pay':
        text_out = 'Не оплатившие аренду'
        mani_menu(call.message.chat.id, who_didnt_pay_menu, text_out)
    elif call.data == 'all' or 'delete' in call.data:
        if 'delete' in call.data:
            del_rent(str(call.data)[7:])
        print_full_list(call.message.chat.id)
    elif call.data == 'stat_menu' or ((call.data in month_list) and location_menu == ''):
        if call.data in month_list:
            month = str(call.data)
        mani_menu(call.message.chat.id, stat_menu,
                  text_start.format(month=month, all=len(get_all_rents()), pay=len(get_who_paid(month)), not_pay=99))
    elif call.data == 'change_month':
        change_month(call.message.chat.id, 'Выберите интересующий месяц')
    elif call.data == 'add_renter':
        bot.send_message(call.message.chat.id, 'Введите наименование арендатора')
        location_menu = 'enter_arendator'
    elif call.data == 'del_renter':
        full_list_renter(call.message.chat.id, 'Выберите арендатора для удаления', 'delete_', 'all')
    elif call.data == 'change':
        pass
    elif ((call.data in month_list) and location_menu == 'enter_month'):
        add_rent(input_name, input_stavka, month_start)
        print_full_list(call.message.chat.id)
        location_menu = ''
    elif call.data == 'set_who_paid':
        full_list_renter(call.message.chat.id, 'Выберите арендатора для внесения арендной платы',
                         'contribute_', 'who_didnt_pay', True)
    elif call.data == 'cansel':
        full_list_renter(call.message.chat.id, 'Выберите арендатора для удаления арендной платы',
                         'cansel_', 'who_paid')
    elif 'contribute_' in call.data:
        location_menu = str(call.data)
        bot.send_message(call.message.chat.id, 'Введите размер платежа')
        print(location_menu[11:])
    elif 'cansel_' in call.data:
        pass


@bot.message_handler(content_types=['text'])
def text_message(message):
    global input_name, location_menu, input_stavka, month_start
    if message.text != '' and location_menu == 'enter_arendator':
        input_name = message.text
        bot.send_message(message.chat.id, 'Введите размер арендной ставки')
        location_menu = 'enter_stavka'
    elif message.text != '' and location_menu == 'enter_stavka':
        input_stavka = int(message.text)
        location_menu = 'enter_month'
        change_month(message.chat.id, 'Выберите месяц начала аренды')
    elif message.text != '' and 'contribute_' in location_menu:
        input_stavka = int(message.text)
        add_contribute(int(location_menu[11:]), input_stavka)
        location_menu = ''
        text_out = 'Не оплатившие аренду'
        mani_menu(message.chat.id, who_didnt_pay_menu, text_out)


check_base()
month = get_month()

bot.polling()


