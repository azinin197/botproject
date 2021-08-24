import telebot
from config import TOKEN, exchanger, ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def start_bot(message: telebot.types.Message):
    text = 'Этот бот помогает перевести одну валюту в другую. \n Для ознакомления со списком валют введите команду /help'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ['help'])
def help_bot(message: telebot.types.Message):
    text = "Список доступных валют доступен по команде /values \n Ввод происходит в формате: \n <базовая валюта>, " \
           "<валюта для ковертации>, <сумма>"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ['values'])
def values_bot(message: telebot.types.Message):
    text = "Доступные валюты"
    for i in exchanger.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types = ['text'])
def convert_bot(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        val1, val2, amount = values
        if len(values) < 3:
            raise ConvertionException("Cлишком мало параметров")
        #val1 - базовая валюта, val2 - валюта конвертации
        result = CryptoConverter.convert(val1, val2, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Не удалось исполнить команду: \n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось исполнить команду: \n{e}")
    else:
        text = f"Текущий курс валюты {val1} в количестве {amount} по отношению к валюте {val2} состовляет: {result}"
        bot.send_message(message.chat.id, text)

bot.polling(none_stop = True, interval = 0)