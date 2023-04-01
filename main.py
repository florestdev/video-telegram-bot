# Импорты.
import sqlite3
from config import *
import telebot
from telebot import types
import random
# Основной код.
bot = telebot.TeleBot(token)
sql = sqlite3.connect('database.db', check_same_thread = False)
db = sql.cursor()
chisles = ["1", "2", "3", "4", "5"]
chislo = random.choice(chisles)

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.chat.id, f'Привет, {message.from_user.full_name}, добро пожаловать в бота, который Флорест сделал в своём видосе!'.format(message.from_user), reply_markup=markup)
	info = sql.execute(f"SELECT * FROM users WHERE id = {message.from_user.id}")
	if info.fetchone() is None:
		db.execute("INSERT INTO users (id, user_name, user_surname, username, balance, win_casino)  VALUES (?, ?, ?, ?, ?, ?)", (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, 0, 0))
		sql.commit()

@bot.message_handler(content_types=['text'])
def main(message):
	if message.text == 'Сыграть в казино.':
		bot.send_message(message.chat.id, f'Я загадаю Вам число от 1 до 5.', reply_markup=markup2)
	if message.text == chislo:
		bot.send_message(message.chat.id, f'Вы правы! Вам насчитано 50 единиц валюты!')
		db.execute(f"UPDATE users SET balance = balance + 50 WHERE id = {message.from_user.id}")
		db.execute(f"UPDATE users SET win_casino = win_casino + 1 WHERE id = {message.from_user.id}")
		sql.commit()
		sql.commit()
		for i_balance in sql.execute(f"SELECT balance FROM users WHERE id = {message.from_user.id}"):
			for i_win in sql.execute(f"SELECT win_casino FROM users WHERE id = {message.from_user.id}"):
				bot.send_message(message.chat.id, f'Ура. У Вас баланс: {i_balance[0]}. Вы выиграли в казино: {i_win[0]}.', reply_markup=markup)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup2 = types.ReplyKeyboardMarkup()
button1 = types.KeyboardButton('Сыграть в казино.')
button2 = types.KeyboardButton('1')
button3 = types.KeyboardButton('2')
button4 = types.KeyboardButton('3')
button5 = types.KeyboardButton('4')
button6 = types.KeyboardButton('5')
markup.add(button1)
markup2.add(button2, button3, button4, button5, button6)

bot.polling(none_stop=True)