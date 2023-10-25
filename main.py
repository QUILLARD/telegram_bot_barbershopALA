from config import BOT_TOKEN
import telebot
from telebot import types

bot = telebot.TeleBot(BOT_TOKEN)

with open('messages/description.txt', 'r', encoding='utf8') as file:
    description = file.read()

with open('messages/price.txt', 'r', encoding='utf8') as file:
    price = file.read()

with open('messages/contacts.txt', 'r', encoding='utf8') as file:
    contacts = file.read()

user_state = {}


def get_main_menu():
    keyboard = types.InlineKeyboardMarkup()
    button_01 = types.InlineKeyboardButton(text='🪄Услуги/💰Цены', callback_data='price')
    button_02 = types.InlineKeyboardButton(text='📅 Запись', callback_data='recording')
    button_03 = types.InlineKeyboardButton(text='✂ Наши работы', callback_data='examples')
    button_04 = types.InlineKeyboardButton(text='📞 Связь', callback_data='contacts')
    keyboard.add(button_01, button_02)
    keyboard.add(button_03, button_04)

    return keyboard


@bot.message_handler(commands=['start'])
def start_message(message):
    user_state[message.chat.id] = 'main_menu'
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, {description}', reply_markup=get_main_menu())


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Вернуться назад', callback_data='back')
    keyboard.add(button)

    if callback.data == 'price':
        user_state[callback.message.chat.id] = 'price'
        bot.send_message(callback.message.chat.id, price, reply_markup=keyboard)
    elif callback.data == 'recording':
        user_state[callback.message.chat.id] = 'recording'
        bot.send_message(callback.message.chat.id, f'Упсс... Меня еще не научили записывать.. Попробуйте позже',
                         reply_markup=keyboard)
    elif callback.data == 'examples':
        user_state[callback.message.chat.id] = 'examples'
        photos = [
            open('examples/1.jpg', 'rb'),
            open('examples/2.jpg', 'rb'),
            open('examples/3.jpg', 'rb')
        ]
        media = [telebot.types.InputMediaPhoto(photo) for photo in photos]
        bot.send_media_group(callback.message.chat.id, media)
        bot.send_message(callback.message.chat.id, f'Примеры работ наших мастеров', reply_markup=keyboard)
    elif callback.data == 'contacts':
        user_state[callback.message.chat.id] = 'contacts'
        bot.send_message(callback.message.chat.id, contacts, reply_markup=keyboard)
    elif callback.data == 'back':
        if user_state.get(callback.message.chat.id) == 'main_menu':
            bot.send_message(callback.message.chat.id, "Вы уже в главном меню.")
        else:
            user_state[callback.message.chat.id] = 'main_menu'
            bot.send_message(callback.message.chat.id, "Вы вернулись в главное меню.", reply_markup=get_main_menu())


if __name__ == '__main__':
    bot.polling(none_stop=True)
