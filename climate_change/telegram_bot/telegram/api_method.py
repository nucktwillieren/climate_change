from .params import *
import requests
import json

def post(data:dict):
    print(data)
    response = requests.post(
        f"{TELEGRAM_URL}{TOKEN}/sendMessage", data=json.dumps(data), headers={'Content-Type': 'application/json'}
    )
    print(response.text)

def send_inline_keyboard(chat_id, text, keyboard):
    
    #inlineKeyboard = [
    #    [
    #        {
    #        'text': 'Google',
    #        "url": 'https://www.google.com.tw/'
    #        }
    #    ],
    #    [
    #        {
    #        'text': 'Yahoo',
    #        'url': 'https://tw.yahoo.com/'
    #        },
    #        {
    #        'text': 'Bing',
    #        'url': 'https://www.bing.com/'
    #        }
    #    ]
    #]
    
    data = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "inline_keyboard": keyboard
        }
    }

    post(data)

def send_message(chat_id,text):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }

    post(data)

    
    