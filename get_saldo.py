import requests

def bot_send_text(bot_message):
    
    bot_token = '5748811715:AAH9EIiQGBpK85wc4sEaZZlbfbHd5ZEOxq0'
    bot_chatID = '9893744'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


def parse_response(response):
    firstElement = response.split("[")[1].split("]")[0].split(",{")[0].split("{")[1].split("}")[0].split(", ")[10].split("saldo : '")[1].split("'")[0]
    return firstElement


def report():
    idTarjeta = '10037097'
    response_API = requests.get('http://www.gpssumo.com/movimientos/get_movimientos/' + idTarjeta)
    # print(response_API.status_code)
    data = response_API.text
    saldo = 'Te quedan ' + parse_response(data) + ' en la tarjeta ' + idTarjeta
    bot_send_text(saldo)


if __name__ == '__main__':
        
    report()
