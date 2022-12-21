from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/ref')
b2 = KeyboardButton('/cancel')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1, b2)