import requests
token = "722519073:AAGz5JXntidyedz1xhxBCaL4k9XxogGx_Tg"
url = "https://api.telegram.org/bot" + token + "/"
reps = 1

while True:
    result = requests.get(url + "getUpdates?offset=610416979&timeout=1").json()['result']
    for message in result:
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
                    message_out = {"chat_id": chat_id, "text": reply}
                    requests.post(url + "sendMessage", json = message_out)
        offset = str(message['update_id'] + 1)
        print(offset)
        result = requests.get(url + "getUpdates?offset=" + offset + "&timeout=1").json()['result']
