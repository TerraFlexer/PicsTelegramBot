import telebot, wikipedia, re, random, os, fnmatch, pathlib, time
import dbhelper as db
from telebot import types

bot = telebot.TeleBot('5324086067:AAEVyQLHE7hV62JPgT0wxABVIT3nQGthai4')
imgpath = "C:\\Users\\gameh\\Documents\\Pics\\"
filepath = "C:\\Users\\gameh\\gameh\\PicsTelegramBot\\"

n = len(fnmatch.filter(os.listdir(imgpath), '*.jpg'))
rating_flag = 0

db.setup_users()
db.setup_pics()

def add_user(id, name):
	db.dbadd_user(id, name)

@bot.message_handler(commands=["start"])
def start(m):
	add_user(m.chat.id, m.from_user.first_name)
	bot.send_message(m.chat.id, 'Начинаем БАЗУ')


@bot.message_handler(commands=["help"])
def help(m):
	add_user(m.chat.id, m.from_user.first_name)
	bot.send_message(m.chat.id, '/start - Начало работы\n/help - помощь\nНапиши "Дай" и бот пришлет фулл\nОтправь боту картинку, и он сохранит ее в БАЗУ\n')


@bot.message_handler(commands=["get_n"])
def get_n(m):
	add_user(m.chat.id, m.from_user.first_name)
	strn = str(n) + '\n'
	bot.send_message(m.chat.id, strn)


@bot.message_handler(regexp="Дай")
def handle_give(message):
	add_user(message.chat.id, message.from_user.first_name)
	name = imgpath + "img"
	num = random.randint(1, n)
	name += str(num) + ".jpg"
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
		bot.send_message(message.chat.id, "Ваш голос учтен", reply_markup=types.ReplyKeyboardRemove())
	else:
		bot.send_message(message.chat.id, "Если вам что - то непонятно, напишите /help")


@bot.message_handler(content_types=['document'])
def handle_document(message):
	add_user(message.chat.id, message.from_user.first_name)
	bot.send_message(message.chat.id, "Принял в БАЗУ")
	global n
	n += 1
	file_info = bot.get_file(message.document.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	src = imgpath + message.document.file_name;
	with open(src, 'wb') as new_file:
		new_file.write(downloaded_file)
	os.rename(src, imgpath + 'img' + str(n) + '.jpg')
	db.dbadd_pic(n, message.chat.id)


@bot.message_handler(content_types=['photo'])
def handle_image(message):
	add_user(m.chat.id)
	bot.send_message(message.chat.id, """Уберите галочку с пункта \"Сжать изображние\" если вы отправляете с ПК,
		или отправьте картинку, как файл, если вы отправляете с телефона""")


bot.polling(none_stop=True, interval=0)