from aiogram import types


def get_standard_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Новый материал')
    item2 = types.KeyboardButton('Новый урок')
    item3 = types.KeyboardButton('Новое слово')
    item4 = types.KeyboardButton('Посмотреть все материалы')
    item5 = types.KeyboardButton('Посмотреть все уроки')
    item6 = types.KeyboardButton('Посмотреть все слова')
    item7 = types.KeyboardButton('Сколько слов записано')
    markup.row(item1, item2, item3)
    markup.row(item4, item5, item6)
    markup.row(item7)
    return markup


def get_first_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начинаем изучать!")
    item2 = types.KeyboardButton("Нет, спасибо")
    markup.add(item1, item2)
    return markup


def get_mark_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('1')
    item2 = types.KeyboardButton('2')
    item3 = types.KeyboardButton('3')
    item4 = types.KeyboardButton('4')
    item5 = types.KeyboardButton('5')
    markup.row(item1, item2, item3, item4, item5)
    return markup
