import telebot, os

import tiktok, twitter

# get path of directory containing bot script
dir = os.path.dirname(os.path.realpath(__file__)) + "/"

# change current working directory to 'dir'
os.chdir(dir)

# open file containing token and read from it
try:
    with open("../files/telegram.txt") as f:
        token = f.readlines()
    f.close()
except OSError:
    print("Open error: Could not open the \'telegram.txt\' file.")

# prepare token and key
token = str(token[0])

# create bot instance
bot = telebot.TeleBot(token)

# handle callback queries
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    globals()[str(call.data)](call.message)

# handle /start command
@bot.message_handler(commands=['start'])
def command_start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    help_button = telebot.types.InlineKeyboardButton(text = "Lista komend 📃", callback_data = "command_help")
    markup.add(help_button)
    bot.send_message(message.chat.id, "Cześć, z tej strony Cezary924Bot! 🤖👋", reply_markup = markup)

# handle /tiktok command
@bot.message_handler(commands=['tiktok'])
def command_tiktok(message):
    bot.send_message(message.chat.id, "Aby pobrać wideo z serwisu TikTok wystarczy, że wyślesz mi do niego link 🎵")

# handle /twitter command
@bot.message_handler(commands=['twitter'])
def command_twitter(message):
    bot.send_message(message.chat.id, "Aby pobrać wideo z serwisu Twitter wystarczy, że wyślesz mi do niego link 🐦")


# handle /help command
@bot.message_handler(commands=['help'])
def command_help(message):
    bot.send_message(message.chat.id, "Oto lista dostępnych poleceń 📃:\n\n" + 
                     "/start - Zaczęcie rozmowy z botem 🤖\n" + 
                     "/help - Lista dostępnych komend 📃\n" +
                     "/about - Informacje o bocie ℹ️\n" +
                     "/tiktok - Pobieranie wideo z serwisu TikTok 🎵\n" +
                     "/twitter - Pobieranie wideo z serwisu Twitter 🐦")

# handle /about command
@bot.message_handler(commands=['about'])
def command_about(message):
    bot.send_message(message.chat.id, "*Cezary924Bot*\n"
                    + "Opis: _Wielofunkcyjny bot na platformie Telegram_\n"
                    + "Wersja: _Beta_\n"
                    + "Autor: _Cezary924_\n"
                    + "Rok powstania: _2023_\n"
                    + "Lata rozwijania: _2023-nadal_", parse_mode= 'Markdown')

# handle TikTok urls
@bot.message_handler(func=lambda message: tiktok.check_tiktok_url(message))
def echo_tiktok(message):
    tiktok.start_tiktok(message, bot)

# handle Twitter urls
@bot.message_handler(func=lambda message: twitter.check_twitter_url(message))
def echo_twitter(message):
    twitter.start_twitter(message, bot)

# handle any other message
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Niestety, nie rozumiem Twojej wiadomości... 💔")

# infinite loop
print("Cezary924-Telegram-Bot has been started.")
bot.infinity_polling()