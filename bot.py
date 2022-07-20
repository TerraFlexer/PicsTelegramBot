import telebot, wikipedia, re, random, os, fnmatch, pathlib
import dbhelper as db

bot = telebot.TeleBot('5324086067:AAEVyQLHE7hV62JPgT0wxABVIT3nQGthai4')
filepath = "C:\\Users\\gameh\\Documents\\"

n = len(fnmatch.filter(os.listdir(filepath), '*.jpg')) - 1

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
	bot.send_message(m.chat.id, '/start - Начало работы\n/help - помощь\nНапиши "Дай" и бот пришлет фулл\nОтправь боту картинку, и он добавит ее в свою БАЗУ\n')


@bot.message_handler(commands=["get_n"])
def get_n(m):
	add_user(m.chat.id, m.from_user.first_name)
	strn = str(n) + '\n'
	bot.send_message(m.chat.id, strn)


@bot.message_handler(regexp="Дай")
def handle_give(message):
	add_user(message.chat.id, message.from_user.first_name)
	name = "C:\\Users\\gameh\\Documents\\img"
	num = random.randint(0, n)
	name += str(num) + ".jpg"
	bot.send_photo(message.chat.id, open(name, 'rb'))


@bot.message_handler(content_types=['document'])
def handle_document(message):
	add_user(message.chat.id, message.from_user.first_name)
	bot.send_message(message.chat.id, "Принял в БАЗУ")
	global n
	n += 1
	file_info = bot.get_file(message.document.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	src = filepath + message.document.file_name;
	with open(src, 'wb') as new_file:
		new_file.write(downloaded_file)
	os.rename(src, 'img' + str(n) + '.jpg')
	db.dbadd_pic(n - 1, message.chat.id)

@bot.message_handler(content_types=['photo'])
def handle_image(message):
	add_user(m.chat.id)
	bot.send_message(message.chat.id, "Уберите галочку с пункта \"Сжать изображние\" если вы с ПК, или отправьте картинку, как файл, если вы с телефона")


bot.polling(none_stop=True, interval=0)
