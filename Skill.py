import telebot
from config import keys, TOKEN
from utils import ConvertionExceptions, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n \
Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        value = message.text.split()
        if len(value) < 3:
            raise ConvertionExceptions('Слишком мало параметров')
        elif len(value) > 3:
            raise ConvertionExceptions('Слишком много параметров')
        quote, base, amount = value
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionExceptions as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
