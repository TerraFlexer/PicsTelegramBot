import telebot, wikipedia, re, random, os, fnmatch, pathlib, time, shutil
import dbhelper as db
from telebot import types

bot = telebot.TeleBot('5324086067:AAEVyQLHE7hV62JPgT0wxABVIT3nQGthai4')
tempimgpath = "C:\\Users\\gameh\\Documents\\Pics\\Temp\\"
imgpath = "C:\\Users\\gameh\\Documents\\Pics\\"
filepath = "C:\\Users\\gameh\\gameh\\PicsTelegramBot\\"

n = len(fnmatch.filter(os.listdir(imgpath), '*.jpg'))
rating_flag = 0

db.setup_users()
db.setup_pics()
db.setup_likes()

def add_user(id, name):
	db.dbadd_user(id, name)


def renaming(uid):
	global n
	res = os.listdir(tempimgpath)
	for file in res:
		n += 1
		print(n)
		os.rename(tempimgpath + str(file), imgpath + 'img' + str(n) + '.jpg')
		db.dbadd_pic(n, uid)


@bot.message_handler(commands=["start"])
def start(m):
	add_user(m.chat.id, m.from_user.first_name)
	bot.send_message(m.chat.id, 'Начинаем БАЗУ')


@bot.message_handler(commands=["help"])
def help(m):
	add_user(m.chat.id, m.from_user.first_name)
	bot.send_message(m.chat.id, """/start - Начало работы\n/help - Список команд\n/top - Топ 3 картинки с лучшим рейтингом\nНапишите "Дай" и бот пришлет фулл\nОтправьту боту картинку, и он сохранит ее в БАЗУ\n""")


@bot.message_handler(commands=["get_n"])
def get_n(m):
	add_user(m.chat.id, m.from_user.first_name)
	strn = str(n) + '\n'
	bot.send_message(m.chat.id, strn)


@bot.message_handler(commands=["top"])
def start(m):
	add_user(m.chat.id, m.from_user.first_name)
	results = db.dbget_top()
	ind = 1
	for row in results:
		num = row[0]
		rate = row[1]
		name = imgpath + "img" + str(num) + ".jpg"
		text = str(ind) + "-е место с рейтингом " + str(rate)
		bot.send_photo(m.chat.id, open(name, 'rb'), caption = text)
		ind += 1
		

@bot.message_handler(regexp="Дай")
def handle_give(message):
	add_user(message.chat.id, message.from_user.first_name)
	if (n == 0):
		bot.send_message(message.chat.id, "Картинок в базе нет, пришлите свои")
		return

	name = imgpath + "img"
	num = random.randint(1, n)
	prev = db.dbget_lastnum(message.chat.id)
	if (n > 1 and num == prev):
		num += 1
		if (num > n):
			num = 1
	name += str(num) + ".jpg"
	db.dbupdate_lastnum(message.chat.id, num)
	markup = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
	likebutn = types.KeyboardButton("like")
	dislkbutn = types.KeyboardButton("dislike")
	markup.add(likebutn, dislkbutn)
	bot.send_photo(message.chat.id, open(name, 'rb'), reply_markup = markup)
	global rating_flag
	rating_flag = 1


@bot.message_handler(content_types=['text'])
def handle_reaction(message):
	add_user(message.chat.id, message.from_user.first_name)
	global rating_flag
	if (rating_flag):
		rating_flag = 0
		if (message.text == "like"):
			rate_change = 1
		elif (message.text == "dislike"):
			rate_change = -1
		pic_id = db.dbget_lastnum(message.chat.id)
		exist = db.dbadd_like(message.chat.id, pic_id, rate_change)
		if (exist == 0):
			db.dbupdate_rating(message.chat.id, pic_id, rate_change)
			rate = db.dbget_rating(pic_id)
			msgtxt = "Ваш голос учтен, текущий рейтинг картинки: " + str(rate)
			bot.send_message(message.chat.id, msgtxt, reply_markup=types.ReplyKeyboardRemove())
		else:
			rate = db.dbget_rating(pic_id)
			msgtxt = "Вы уже оценивали эту картинку, текущий рейтинг картинки: " + str(rate)
			bot.send_message(message.chat.id, msgtxt, reply_markup=types.ReplyKeyboardRemove())
	else:
		bot.send_message(message.chat.id, "Если вам что - то непонятно, напишите /help")


@bot.message_handler(content_types=['document'])
def handle_document(message):
	add_user(message.chat.id, message.from_user.first_name)
	bot.send_message(message.chat.id, "Принял в БАЗУ")
	file_info = bot.get_file(message.document.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	src = tempimgpath + message.document.file_name;
	with open(src, 'wb') as new_file:
		new_file.write(downloaded_file)
	renaming(message.chat.id)


@bot.message_handler(content_types=['photo'])
def handle_image(message):
	add_user(m.chat.id)
	bot.send_message(message.chat.id, """Уберите галочку с пункта \"Сжать изображние\" если вы отправляете с ПК,
		или отправьте картинку, как файл, если вы отправляете с телефона""")


bot.polling(none_stop=True, interval=0)