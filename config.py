import json
import requests

TOKEN = "1902703715:AAGazcJm5gQXvaTepxomc4p72vKYYklnBLU"


exchanger = {
    'доллар' : 'USD',
    'рубль' : 'RUB',
    'евро' : 'EUR',
    'йена' : 'JPY'
}


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(val1:str, val2:str, amount:str):
        if val1 == val2:
            raise ConvertionException(f"Невозможно конвертировать одинаковые валюты {exchanger[val1]}")

        try:
            val1_ticker = exchanger[val1]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {val1}")

        try:
            val2_ticker = exchanger[val2]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {val2}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException("Неверно введено количество")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={val1_ticker}&tsyms={val2_ticker}")
        result = float(json.loads(r.content)[exchanger[val2]]) * amount
        return result

