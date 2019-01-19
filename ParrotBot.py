import requests
token = "722519073:AAGz5JXntidyedz1xhxBCaL4k9XxogGx_Tg"
url = "https://api.telegram.org/bot" + token + "/"
while True:
    result = requests.get(url + "getUpdates?offset=610416947&timeout=1").json()['result']
    for message in result:
        chat_id = message['message']['chat']['id']
        if 'text' in message['message']:
            reply = message['message']['text']
            message_out = {"chat_id": chat_id, "text": reply}
            requests.post(url + "sendMessage", json = message_out)
        offset = str(message['update_id'] + 1)
        print(offset)
        result = requests.get(url + "getUpdates?offset=" + offset + "&timeout=1").json()['result']
