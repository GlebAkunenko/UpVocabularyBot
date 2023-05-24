from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

start = ReplyKeyboardMarkup(
	resize_keyboard=True,
	one_time_keyboard=True
)

start.add(KeyboardButton("Отправить словарь"))

cancel = InlineKeyboardMarkup(
	[[InlineKeyboardButton("Отмена", callback_data='CANC')]]
)

choose = InlineKeyboardMarkup( [
	[InlineKeyboardButton("Обычный", callback_data='1')],
	[InlineKeyboardButton("Обратный", callback_data='2')]
])