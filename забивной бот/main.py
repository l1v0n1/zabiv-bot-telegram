import logging
from aiogram import Bot, Dispatcher, executor, types
import sqlite3
import keyboard as kb
from config import API_TOKEN, admin, admin_name
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import random
from aiogram.utils.exceptions import Throttled
import emoji as emo
import os

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

connection = sqlite3.connect('data.db')
q = connection.cursor()

class info(StatesGroup):
	name = State()
	rasst = State()

async def antiflood(*args, **kwargs):
    m = args[0]
    await m.answer("⏳ Ходить на забивы можно раз в 15 секунд...")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	q.execute(f"SELECT * FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchall()
	if len(result) == 0:
		q.execute(f"INSERT INTO users (user_id, win)"
					f"VALUES ('{message.chat.id}', '0')")
		connection.commit()
		await message.answer('Здарова, хлюпик.\nЗдесь забиваются самые отбитые пацанчики.\n\nНу ка, введи тут своё погоняло:')
		await info.name.set()
	else:
		await message.answer('Здарова, хлюпик.\nЗдесь забиваются самые отбитые пацанчики.', reply_markup=kb.keyboard)

@dp.message_handler(state=info.name)
async def name(message: types.Message, state: FSMContext):
	res = q.execute("SELECT name FROM users WHERE lower(name) LIKE lower('{}')".format(message.text)).fetchall()
	if len(res) == 0:
		if len(message.text) <= 20:
			q.execute('UPDATE users SET name = ? WHERE user_id = ?', (message.text, message.chat.id))
			connection.commit()
			await message.answer('Хорошо, буду звать тебя {}'.format(message.text), reply_markup=kb.keyboard)
			await state.finish()
		else:
			await message.answer('Придумай кличку по короче, до 20 символов..')
	else:
		await message.answer('Данное погоняло уже занято, попробуй другое.')

@dp.message_handler(commands=['admin'])
async def adminstration(message: types.Message):
	if message.chat.id == admin:
		await message.answer('Добро пожаловать в админ панель.', reply_markup=kb.apanel)
	else:
		await message.answer('Черт! Ты меня взломал :(')

@dp.callback_query_handler(lambda call: call.data.startswith('rass'))    
async def usender(call):
	await call.message.answer('Введите текст для рассылки.\n\nДля отмены нажмите кнопку ниже 👇', reply_markup=kb.back)
	await info.rasst.set()

@dp.message_handler(state=info.rasst)
async def process_name(message: types.Message, state: FSMContext):
	q.execute(f'SELECT user_id FROM users')
	row = q.fetchall()
	connection.commit()
	if message.text == 'Отмена':
		await message.answer('Отмена! Возвращаю в главное меню.', reply_markup=kb.keyboard)
		await state.finish()
	else:
		info = row
		await message.answer('Начинаю рассылку...')
		for i in range(len(info)):
			try:
				await bot.send_message(info[i][0], str(message.text))
			except:
				pass
		await message.answer('Рассылка завершена.', reply_markup=kb.keyboard)
		await state.finish()


@dp.message_handler(content_types=['text'], text='📰 Профиль')
async def stats(message: types.Message):
	n = q.execute(f'SELECT name FROM users WHERE user_id = {message.chat.id}').fetchone()
	z = q.execute(f'SELECT win FROM users WHERE user_id = {message.chat.id}').fetchone()
	connection.commit()
	name = n[0]
	wins = z[0]
	await message.answer(f'Вот твои данные, салага:\n🆔: {message.chat.id}\n📋 Кличка: {name}\n🏆 Авторитет: {wins}', reply_markup=kb.keyboard)

@dp.message_handler(content_types=['text'], text='ℹ️ Помощь')
async def help(message: types.Message):
	link = f'tg://user?id={admin}'
	await message.answer(f'Тебе набили ебало в забиве? Хочешь спросить главного оффника о чем-либо?\nТебе сюда - {admin_name}', reply_markup=kb.keyboard)

@dp.message_handler(content_types=['text'], text='👊 Забив')
@dp.throttled(antiflood, rate=15)
async def fight(message: types.Message, state: FSMContext):
	chance = random.randint(0, 5)
	if chance in [1, 3, 5]:
		p = random.choice(os.listdir("images/"))
		photo = f'images/{p}'
		with open(photo, 'rb') as file:
			rnd = random.randint(1,10)
			q.execute('UPDATE users SET win = win + {} WHERE user_id = {}'.format(rnd, message.chat.id))
			connection.commit()
			await bot.send_photo(message.chat.id, file, caption='🥇 Забивчик удался, А-У-Е!\nТвой авторитет поднялся: +{}'.format(rnd))
			file.close()
	else:
		rnds = random.randint(1,6)
		q.execute('UPDATE users SET win = win - {} WHERE user_id = {}'.format(rnds, message.chat.id))
		connection.commit()
		await message.answer('Тебя разъебали на забиве..\nТы падаешь в глазах братвы: -{}'.format(rnds))

@dp.message_handler(content_types=['text'], text='🏆 Авторитеты')
async def rating(message: types.Message):
	q.execute(f"SELECT user_id, name, win FROM users order by win desc")
	res = q.fetchall()
	one = emo.emojize(':one:', use_aliases=True)
	two = emo.emojize(':two:', use_aliases=True)
	three = emo.emojize(':three:', use_aliases=True)
	four = emo.emojize(':four:', use_aliases=True)
	five = emo.emojize(':five:', use_aliases=True)
	six = emo.emojize(':six:', use_aliases=True)
	seven = emo.emojize(':seven:', use_aliases=True)
	eight = emo.emojize(':eight:', use_aliases=True)
	nine = emo.emojize(':nine:', use_aliases=True)
	ten = emo.emojize(':ten:', use_aliases=True)
	zero = emo.emojize(':zero:', use_aliases=True)
	em = {0: zero, 1: one, 2: two, 3: three, 4: four, 5: five, 6: six, 7: seven, 8: eight, 9: nine, 10: ten}
	message_lines = []
	for index, item in enumerate(res, 1):

		message_lines.append(f"{em.get(index)} [{item[1]}](tg://user?id={item[0]}): {item[2]} рейтинга")
	am = message_lines[:10]
	mes = '\n'.join(am)
	await message.answer(f'Самые блатные пацаны:\n{mes}', parse_mode='Markdown')


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True) # Запуск