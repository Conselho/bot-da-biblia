import os

import requests as requests

url = 'http://api.telegram.org/bot' + str(os.environ.get('BOT_BIBLIA_API_TOKEN')) + '/'
print('base url:', url)


def get_update_id(update):
    return update["update_id"]


def get_chat_id(update):
    return update["message"]["chat"]["id"]


def get_message_text(update):
    try:
        return update["message"]["text"]
    except KeyError:
        return ""


def last_update(last_solved_update_id):
    # response = requests.get(url + "getUpdates", data={"offset": str(last_solved_update_id)}).json()
    # # se o que está em cima não funcionar, usar antes esta linha
    response = requests.get(url + "getUpdates?offset=" + str(last_solved_update_id)).json()

    result = response["result"]  # result é uma lista de mensagens (updates)
    total_updates = len(result)
    return result[total_updates - 1]


def send_message(chat_id, message_text):
    # params = {"chat_id": chat_id, "text": message_text}
    # return requests.post(url + "sendMessage", data=params)
    # # se o que está em cima não funcionar, usar antes esta linha
    return requests.post(url + "sendMessage?chat_id=" + str(chat_id) + "&text=" + message_text)
