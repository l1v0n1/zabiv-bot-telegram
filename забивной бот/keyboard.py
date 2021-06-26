from aiogram import types

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(
	types.KeyboardButton('📰 Профиль'),
	types.KeyboardButton('👊 Забив'),
	types.KeyboardButton('🏆 Авторитеты')
	)
keyboard.add(types.KeyboardButton('ℹ️ Помощь'))


apanel = types.InlineKeyboardMarkup(row_width=3)
apanel.add(
	types.InlineKeyboardButton(text='Рассылка', callback_data='rass')
    )

back = types.ReplyKeyboardMarkup(resize_keyboard=True)
back.add(
    types.KeyboardButton('Отмена')
)