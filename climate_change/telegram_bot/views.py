from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from .telegram.api_models import Update
from .telegram.api_method import send_inline_keyboard, send_message
from .telegram.params import *
import json


# Create your views here.

@csrf_exempt
def web_hook(request):
    if request.method == "POST":
        t_d = json.loads(request.body.decode())
        data = Update.json_deserializer(t_d)
        if data.message != None:
            if data.message.text == '/test':
                send_message(data.message.chat_belong_to.id,'https://zh.wikipedia.org/wiki/%E6%B0%A3%E5%80%99%E8%AE%8A%E9%81%B7')
            elif data.message.text == '/data':
                pass
            elif data.message.text == '/help':
                pass
            else:
                send_message(data.message.chat_belong_to.id,data.message.text)

        if data.callback_query != None:
            if data.callback_query.data != None:
                pass

    return JsonResponse({'status':'ok'},safe=False)