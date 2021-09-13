import os

import requests as requests

url = 'http://api.telegram.org/bot'+os.environ.get('BOT_BIBLIA_API_TOKEN')+'/'
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
    params = {"offset": str(last_solved_update_id)}
    response = requests.get(url + "getUpdates", data=params).json()
    result = response["result"]  # result é uma lista
    total_updates = len(result)
    return result[total_updates - 1]


def send_message(chat_id, message_text):
    return requests.post(url+"sendMessage?chat_id="+str(chat_id)+"&text="+message_text)
    # # não sei porque é que isto não dá... mas era lindo
    # params = {
    #     "chat_id": chat_id,
    #     "text": message_text
    # }
    # return requests.post(url + "sendMessage", data=params)
