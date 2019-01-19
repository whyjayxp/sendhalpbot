import requests
token = "722519073:AAGz5JXntidyedz1xhxBCaL4k9XxogGx_Tg"
url = "https://api.telegram.org/bot" + token + "/"
MAX_QNS = 5

def generateList(qns):
    text = "<b>Send Halp Questions</b>"
    count = 1
    for qn in qns:
        text += "\n\n" + str(count) + ". " + qn['question'] + "\n"
        text += "[" + str(len(qn['answer'])) + " Ans]"
        count = count + 1
    return text

def main():
    questions = {}
    # questions is a dictionary with chat_id keys. Each key has an array (list) of
    # 5 qn dictionary, that contains a question string, user_id and an array (list)
    # of answer strings
    while True:
        result = requests.get(url + "getUpdates").json()
        if 'result' not in result:
            continue
        result = result['result']
        if len(result) == 0:
            continue # no results :(
        for message in result:
            if 'message' in message: # Message
                chat_id = message['message']['chat']['id']
                if chat_id not in questions:
                    questions[chat_id] = []
                chat_qns = questions[chat_id]

                if 'text' in message['message']: # Text
                    reply = message['message']['text']
                    args = reply.split(" ")
                    if args[0] == "/list":
                        if len(chat_qns) == 0:
                            text = "No questions to show! Ask one using /ask!"
                            message_out = {"chat_id": chat_id, "text": text}
                        else:
                            text = generateList(chat_qns)
                            buttons = [{"text": "1", "callback_data": "1"}]
                            for i in range(2, len(chat_qns) + 1):
                                buttons.append({"text": str(i), "callback_data": str(i)})
                            options = {"inline_keyboard": [buttons]}
                            message_out = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "reply_markup": options}
                        requests.post(url + "sendMessage", json = message_out)

                    elif args[0] == "/remove":
                        user_id = message['message']['from']['id']
                        if len(chat_qns) < int(args[1]):
                            text = "No such question to be removed! Please try again with another index!"
                        elif user_id != chat_qns[int(args[1])]['user_id']:
                            text = "Sorry, you are not allowed to remove this question!"
                        else:
                            del chat_qns[int(args[1])]
                            text = "Question " + args[1] + " has been removed!"
                        message_out = {"chat_id": chat_id, "text": text}
                        requests.post(url + "sendMessage", json = message_out)

                    elif args[0] == "/resolve":
                        user_id = message['message']['from']['id']
                        if len(chat_qns) < int(args[1]):
                            text = "No such question to be resolved! Please try again with another index!"
                        elif user_id != chat_qns[int(args[1])]['user_id']:
                            text = "Sorry, you are not allowed to resolve this question!"
                        else:
                            del chat_qns[int(args[1])]
                            text = "Question " + args[1] + " has been resolved! Congratulationssss"
                        message_out = {"chat_id": chat_id,"text": text}
                        requests.post(url + "sendMessage", json = message_out)
                        
                    elif args[0] == "/answer":
                        continue

                    elif args[0] == "/ping":
                        message_out = {"chat_id": chat_id, "text": "pong"}
                        requests.post(url + "sendMessage", json = message_out)

                    elif args[0] == "/ask":
                        if len(chat_qns) >= MAX_QNS:
                            text = "The maximum questions we can store is " + MAX_QNS + ". Please /remove or /resolve the existing questions first."
                            message_out = {"chat_id": chat_id, "text": text}
                            requests.post(url + "sendMessage", json = message_out)
                        elif len(args) == 1:
                            text = "Please write a question!"
                            message_out = {"chat_id": chat_id, "text": text}
                            requests.post(url + "sendMessage", json = message_out)
                        else:
                            newQn = " ".join(args[1:])
                            user_id = message['message']['from']['id']
                            chat_qns.append({"question": newQn, "answer": [], "user_id": user_id})
                            # x = []
                            #for question in questions:
                            #    x.append([{"text": question, "callback_data": "you finally work!!!"}])
                            #options = {
                            #    "inline_keyboard": x
                            #}
                            text = generateList(chat_qns)
                            buttons = [{"text": "1", "callback_data": "1"}]
                            for i in range(2, len(chat_qns) + 1):
                                buttons.append({"text": str(i), "callback_data": str(i)})
                            options = {"inline_keyboard": [buttons]}
                            message_out = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "reply_markup": options}
                            requests.post(url + "sendMessage", json = message_out)

            elif 'callback_query' in message:
                callback_id = message['callback_query']['id']
                # print("Callback by " + callback_id)
                message_out = {"callback_query_id": callback_id,
                               "text": message['callback_query']['data']}
                requests.post(url + "answerCallbackQuery", json = message_out)

            offset = str(message['update_id'] + 1)
            result = requests.get(url + "getUpdates?offset=" + offset + "&timeout=1").json()['result']

if __name__ == "__main__":
    main()
