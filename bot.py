from config import TOKEN
import telebot
from database import cursor
from telebot import types
from sql.tablets_sql import tabletSQL
from sql.ointments_sql import ointSQL
from sql.syrups_sql import syrupSQL
from datetime import datetime

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    text = f"""
    Здравствуйте, {message.chat.first_name}, вас приветствует Pharmacy_bot!
    """
    markup = types.InlineKeyboardMarkup()
    medicines = types.InlineKeyboardButton('Лекарства', callback_data='medicines')
    ordering = types.InlineKeyboardButton('Добавить лекарство', callback_data="order")
    markup.row_width = 2
    markup.add(medicines, ordering)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == "back")
def answer_conatcts_callback(call):
    message = call.message
    if call.data == "back":
        send_welcome_message(message)

@bot.callback_query_handler(func= lambda call: call.data=='order')
def get_info(call):
    message = call.message
    bot.send_message(chat_id=message.chat.id,
                     text = 'Напишите название лекарства, которое хотите заказать')

    bot.register_next_step_handler(message, add_order_review)

def add_order_review(message):
    medicine = message.text
    user = message.from_user.username
    message_time = message.date
    created = datetime.fromtimestamp(message_time).strftime('%d-%m-%Y %H:%M:%S')
    with open('orders.txt', 'a', encoding='utf-8') as file:
        info = f"""
                Дата создания отзыва: {created}
                Имя пользователя: {user}
                Лекарство: {medicine}
                """
        file.write(info)
    bot.send_message(message.chat.id, text="Спасибо, мы с вами свяжемся в течении недели!")



@bot.callback_query_handler(func= lambda call: call.data=='medicines')
def send_all_genres(call):
    message = call.message
    markup = types.InlineKeyboardMarkup()
    tablets = types.InlineKeyboardButton('Таблетки', callback_data='tablets')
    ointments = types.InlineKeyboardButton('Мази', callback_data='ointments')
    syrups = types.InlineKeyboardButton('Сиропы', callback_data='syrups')
    back_button = types.InlineKeyboardButton('Назад',callback_data='back')
    markup.row_width = 2
    markup.add(tablets,ointments,syrups,back_button)
    bot.edit_message_text(
        chat_id=message.chat.id,
        text="Выберите тип лекарства",
        message_id=message.id,
        reply_markup=markup)

@bot.callback_query_handler(func= lambda call: call.data=='tablets')
def send_all_tablets(call):
    message = call.message
    tablets_manager = tabletSQL(cursor=cursor)
    tablets = tablets_manager.extract_all_data()
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    for id,name,price,description in tablets:
        print(id)
        button = types.InlineKeyboardButton(name, callback_data=f'tablet_{id}')
        markup.add(button)
    button2 = types.InlineKeyboardButton('Назад', callback_data='tablets_back')
    markup.add(button2)
    bot.edit_message_text(
    chat_id=message.chat.id,
    text="Выберите лекарство",
    message_id=message.id,
    reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "tablets_back")
def answer_tablets_callback(call):
    if call.data == "tablets_back":
        send_all_genres(call)


@bot.callback_query_handler(func= lambda call: str(call.data).startswith("tablet_"))
def send_tablet_info(call):
    message = call.message
    id = str(call.data).split("_")[1]
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    manager = tabletSQL(cursor=cursor)
    tablet = manager.extract_one_tablet(int(id))[0]
    text = f"""
        {tablet[0]}
        {tablet[1]}
        {tablet[2]}
        {tablet[3]}
    """
    button2 = types.InlineKeyboardButton('Назад', callback_data='tablets_info_back')
    markup.add(button2)
    bot.edit_message_text(
        chat_id=message.chat.id,
        text=text,
        message_id=message.id,
        reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "tablets_info_back")
def answer_tablet_callback(call):
    if call.data == "tablets_info_back":
        send_all_tablets(call)






@bot.callback_query_handler(func= lambda call: call.data=='ointments')
def send_all_ointments(call):
    message = call.message
    ointments_manager = ointSQL(cursor=cursor)
    ointments = ointments_manager.extract_all_data()
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    for id,name,price,description in ointments:
        print(id)
        button = types.InlineKeyboardButton(name, callback_data=f'ointment_{id}')
        markup.add(button)
    button2 = types.InlineKeyboardButton('Назад', callback_data='ointments_back')
    markup.add(button2)
    bot.edit_message_text(
    chat_id=message.chat.id,
    text="Выберите лекарство",
    message_id=message.id,
    reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "ointments_back")
def answer_ointments_callback(call):
    if call.data == "ointments_back":
        send_all_genres(call)

@bot.callback_query_handler(func= lambda call: str(call.data).startswith('ointment_'))
def send_ointment_info(call):
    message = call.message
    print(call.data)
    id = str(call.data).split("_")[1]
    manager = ointSQL(cursor=cursor)
    ointment = manager.extract_one_ointment(int(id))[0]
    text = f"""
        {ointment[0]}
        {ointment[1]}
        {ointment[2]}
        {ointment[3]}
    """
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    button2 = types.InlineKeyboardButton('Назад', callback_data='ointments_info_back')
    markup.add(button2)
    bot.edit_message_text(
        chat_id=message.chat.id,
        text=text,
        message_id=message.id,
        reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == "ointments_info_back")
def answer_syrups_callback(call):
    if call.data == "ointments_info_back":
        send_all_ointments(call)







@bot.callback_query_handler(func= lambda call: call.data=='syrups')
def send_all_syrups(call):
    message = call.message
    syrups_manager = syrupSQL(cursor=cursor)
    syrups = syrups_manager.extract_all_data()
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    for id,name,price,description in syrups:
        button = types.InlineKeyboardButton(name, callback_data=f'syrup_{id}')
        markup.add(button)
    button2 = types.InlineKeyboardButton('Назад', callback_data='syrups_back')
    markup.add(button2)
    bot.edit_message_text(
    chat_id=message.chat.id,
    text="Выберите лекарство",
    message_id=message.id,
    reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == "syrups_back")
def answer_syrups_callback(call):
    if call.data == "syrups_back":
        send_all_genres(call)



@bot.callback_query_handler(func= lambda call: str(call.data).startswith("syrup_"))
def send_syrup_info(call):
    message = call.message
    print(call.data)
    id = str(call.data).split("_")[1]
    manager = syrupSQL(cursor=cursor)
    syrup = manager.extract_one_syrup(int(id))[0]
    text = f"""
        {syrup[0]}
        {syrup[1]}
        {syrup[2]}
        {syrup[3]}
    """
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    button2 = types.InlineKeyboardButton('Назад', callback_data='syrups_info_back')
    markup.add(button2)
    bot.edit_message_text(
        chat_id=message.chat.id,
        text=text,
        message_id=message.id,
        reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "syrups_info_back")
def answer_syrups_callback(call):
    if call.data == "syrups_info_back":
        send_all_syrups(call)


bot.infinity_polling()