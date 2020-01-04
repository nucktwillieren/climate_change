from django.urls import path
from .views import web_hook
from .telegram.params import TOKEN

app_name = 'telegram_bot'

urlpatterns = [
    path(f'{TOKEN}/',web_hook,name='web_hook'),
]