# button.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [
    ['Ariza berish📎'],
    # ["Arizani olib tashlash❌"]
]

for row in buttons:
    menu_keyboard.add(*(KeyboardButton(text) for text in row))

tuman_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
tuman_buttons = [
    ['Angor tumani', 'Bandixon tumani'],
    ['Boysun tumani', 'Denov tumani'],
    ['Jarqoʻrgʻon tumani', 'Qiziriq tumani'],
    ['Qumqoʻrgʻon tumani', 'Muzrabod tumani'],
    ['Oltinsoy tumani', 'Sariosiyo tumani'],
    ['Sherobod tumani', 'Shoʻrchi tumani'],
    ['Termiz tumani', 'Uzun tumani']
]

for row in tuman_buttons:
    tuman_keyboard.add(*(KeyboardButton(text) for text in row))
