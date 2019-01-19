import requests
token = "722519073:AAGz5JXntidyedz1xhxBCaL4k9XxogGx_Tg"
url = "https://api.telegram.org/bot" + token + "/"
reps = 1
 
while True:
    result = requests.get(url + "getUpdates?offset=610416985&timeout=1").json()['result']
    if len(result) == 0:
        continue
    for message in result:
        if 'message' in message:
            chat_id = message['message']['chat']['id']
            if 'text' in message['message']:
                reply = message['message']['text']
                args = reply.split(" ")
                if args[0] == "/reps":
                    if len(args) == 2:
                        reps = int(args[1])
                        message_out = {"chat_id": chat_id, "text": "Echo " + args[1] + " times"}
                    else:
                        message_out = {"chat_id": chat_id, "text": "Incorrect command"}
                    requests.post(url + "sendMessage", json = message_out)
                elif args[0] == "/echo":
                    reply = " ".join(args[1:])
                    for i in range(1, reps + 1):
                        options = {"inline_keyboard": [[{"text": "Hi", "callback_data": "hello"}], [{"text": "Bye", "callback_data": "byebye"}]]}
                        message_out = {"chat_id": chat_id, "text": reply, "reply_markup": options}
                        requests.post(url + "sendMessage", json = message_out)
        elif 'callback_query' in message:
            print("Callback!")
            callback_id = message['callback_query']['id']
            message_out = {"callback_query_id": callback_id, "text": message['callback_query']['data']}
            requests.post(url + "answerCallbackQuery", json = message_out)

        offset = str(message['update_id'] + 1)
        print(offset)
        result = requests.get(url + "getUpdates?offset=" + offset + "&timeout=1").json()['result']
