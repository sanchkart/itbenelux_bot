import json
from botocore.vendored import requests
import os
import re

BOT_TOKEN = os.environ['bot_token']
URL = "https://api.telegram.org/bot{}/".format(BOT_TOKEN)
STIKER = os.environ['sticker']

def join_handler(chat_id, reply_to):
    send_message("Игорь, ты ли это?", chat_id, reply_to)

def send_message(text, chat_id,reply_to):
    url = URL + "sendMessage"
    payload={'chat_id':chat_id,'text':text}
    if reply_to:
        payload['reply_to_message_id']=reply_to
    requests.post(url, json=payload)
def send_sticker(sticker_id, chat_id, reply_to):
    print("sending sticker %s %s %s"%(sticker_id, chat_id, reply_to))
    url = URL + "sendSticker"
    payload={'chat_id':chat_id,'sticker':sticker_id}
    if reply_to:
        payload['reply_to_message_id']=reply_to
    r = requests.post(url, json=payload)
    print(r.json())

def lambda_handler(event, context):
    message = json.loads(event['body'])
    print(message)
    try:
        if message['message']['new_chat_participant']['id']:
            print('new member')
            chat_id = message['message']['chat']['id']
            reply_to = message['message']['message_id']
            join_handler(chat_id,reply_to)  
    except:
        pass
    
    try:
        body_message = message['message']
    except:
        try:
            print("edited message")
            body_message = message['edited_message']
        except:
            print("wrong message type")
            return
    try:
        p = re.compile(r".*я .*ору.*", re.IGNORECASE)
        message_text = (body_message['text']).lower()
        if p.match(message_text):
            print("chat message")
            chat_id = body_message['chat']['id']
            reply_to = body_message['message_id']
    
            sticker_id = STIKER
            send_sticker(sticker_id, chat_id, reply_to)
    except:
        pass
    return {
        'statusCode': 200
    }