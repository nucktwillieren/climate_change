from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .models import TelegramChat, Knowledge, Policy
from .telegram.api_models import Update
from .telegram.api_method import send_inline_keyboard, send_message, send_keyboard, send_html_message
from .telegram.params import *
from .crawler import get_list, target, source, get_help, help_target
import json
import random
import time

# Create your views here.

@csrf_exempt
def web_hook(request):
    if request.method == "POST":
        t_d = json.loads(request.body.decode())
        data = Update.json_deserializer(t_d)
        if data.message != None:
            if data.message.text == '/test':
                send_message(data.message.chat_belong_to.id,'https://zh.wikipedia.org/wiki/%E6%B0%A3%E5%80%99%E8%AE%8A%E9%81%B7')
            elif data.message.text == '/trivia':
                chat_room,_ = TelegramChat.objects.get_or_create(chat_id=data.message.chat_belong_to.id)
                
                has_seen = chat_room.knowledge_pack.all()
                print(has_seen)
                pack_num = Knowledge.objects.count()
                if pack_num != 0:
                    random_num = random.randint(1,pack_num)
                    k = Knowledge.objects.get(id=random_num)
                    send_message(chat_room.chat_id, "*{}* ```{}```".format(k.title,k.description))
                    send_inline_keyboard(
                        data.message.chat_belong_to.id,
                        "Give Us A Feedback",
                        [
                            [
                                {
                                    'text':"Like","callback_data":'trivia.like.{}.{}'.format(k.knowledge_code,chat_room.chat_id)
                                },
                                {
                                    'text':"So So","callback_data":'trivia.so_so.{}.{}'.format(k.knowledge_code,chat_room.chat_id)
                                },
                                {
                                    'text':"Unlike","callback_data":'trivia.unlike.{}.{}'.format(k.knowledge_code,chat_room.chat_id)
                                }
                            ]
                        ]
                    )
            elif data.message.text == '/policy':
                chat_room,_ = TelegramChat.objects.get_or_create(chat_id=data.message.chat_belong_to.id)
                
                has_seen = chat_room.policy_pack.all()
                print(has_seen)
                pack_num = Policy.objects.count()
                if pack_num != 0:
                    random_num = random.randint(1,pack_num)
                    k = Policy.objects.get(id=random_num)
                    send_message(chat_room.chat_id, "*{}* ```{}``` [See More Here]({})".format(k.title,k.description,k.url))
                    send_inline_keyboard(
                        data.message.chat_belong_to.id,
                        "Give Us A Feedback",
                        [
                            [
                                {
                                    'text':"Like","callback_data":'policy.like.{}.{}'.format(k.policy_code,chat_room.chat_id)
                                },
                                {
                                    'text':"So So","callback_data":'policy.so_so.{}.{}'.format(k.policy_code,chat_room.chat_id)
                                },
                                {
                                    'text':"Unlike","callback_data":'policy.unlike.{}.{}'.format(k.policy_code,chat_room.chat_id)
                                }
                            ]
                        ]
                    )
                else:
                    pass
            elif data.message.text == '/headline':
                chat_room,_ = TelegramChat.objects.get_or_create(chat_id=data.message.chat_belong_to.id)
                news = get_list()[1]
                send_message(chat_room.chat_id, "*{}* ```{}``` ```{}``` [See More Here]({})".format(news['title'],news['date'],news['content'],source+news['url']))
                send_inline_keyboard(
                    data.message.chat_belong_to.id,
                    "Give Us A Feedback",
                    [
                        [
                            {
                                'text':"Like","callback_data":'news.like.{}.{}'.format("",chat_room.chat_id)
                            },
                            {
                                'text':"So So","callback_data":'news.so_so.{}.{}'.format("",chat_room.chat_id)
                            },
                            {
                                'text':"Unlike","callback_data":'news.unlike.{}.{}'.format("",chat_room.chat_id)
                            }
                        ]
                    ]
                )
            elif data.message.text == '/push_weather_like_a_god':
                chat_rooms = TelegramChat.objects.all()
                helper_content = get_help()
                for chat_room in chat_rooms:
                    send_message(chat_room.chat_id, helper_content)
                    time.sleep(.1)

            elif data.message.text == '/weather':
                chat_room,_ = TelegramChat.objects.get_or_create(chat_id=data.message.chat_belong_to.id)
                helper_content = get_help()
                send_message(
                    chat_room.chat_id, 
                    helper_content
                )

            elif data.message.text == '/push_headline_like_a_god':
                chat_rooms = TelegramChat.objects.all()
                news = get_list()[1]
                for chat_room in chat_rooms:
                    send_message(chat_room.chat_id, "*[Headline Today]* *{}* ```{}``` ```{}``` [See More Here]({})".format(news['title'],news['date'],news['content'],source+news['url']))
                    send_inline_keyboard(
                        data.message.chat_belong_to.id,
                        "Give Us A Feedback",
                        [
                            [
                                {
                                    'text':"Like","callback_data":'news.like.{}.{}'.format("",chat_room.chat_id)
                                },
                                {
                                    'text':"So So","callback_data":'news.so_so.{}.{}'.format("",chat_room.chat_id)
                                },
                                {
                                    'text':"Unlike","callback_data":'news.unlike.{}.{}'.format("",chat_room.chat_id)
                                }
                            ]
                        ]
                    )
                    time.sleep(.2)
            elif data.message.text == '/start':
                TelegramChat.objects.get_or_create(chat_id=data.message.chat_belong_to.id)
                send_message(data.message.chat_belong_to.id,"Hello~")
                #send_keyboard(data.message.chat_belong_to.id,'Hello',None)
            elif data.message.text == '/help':
                pass
            else:
                send_message(data.message.chat_belong_to.id,data.message.text)

        if data.callback_query != None:
            if data.callback_query.data != None:
                pass

    return JsonResponse({'status':'ok'},safe=False)