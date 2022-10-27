import os
import json
import traceback
import uuid
from django.http import HttpResponse
import telegram
from emoji import emojize
from bot.cred import *
from django.views.decorators.csrf import csrf_exempt
from bot.utils import get_city_name, get_lat_lon, get_weather_details, reply_weather_info


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token= TOKEN)
'''{"update_id":593872375,\n"message":{"message_id":2749,"from":{"id":5164975159,"is_bot":false,"first_name":"N","last_name":"R","language_code":"en"},
"chat":{"id":5164975159,"first_name":"N","last_name":"R","type":"private"},"date":1652994955,"text":"Hi"}}'''
@csrf_exempt
def home(request):
    try:
        body = json.loads(request.body)
        print(body)
        filename = None
        chat_id = body.get('message').get('chat').get('id')
        print(chat_id)
        text = body.get('message').get('text')
        location = body.get('message').get('location')
        reply_message_id = body.get('message').get('message_id')
        reply_text = 'Welcome to Weather Information Bot! {} {}{}\n Send me a location or the name of a place with the word "weather", eg- weather delhi, and I will send you the weather update.'.format(body.get('message').get('from').get('first_name'),body.get('message').get('from').get('last_name'),emojize(':grinning_face:'))
        text = str(text)
        if (chat_id != 5164975159):
            bot.send_message(chat_id=5164975159, text=('From: {} {}\nMessage: {}'.format(body.get('message').get('from').get('first_name'),body.get('message').get('from').get('last_name'),text)))
    
        if 'weather' in text.lower():
            filename = str(uuid.uuid4())
            city_name = text.lower().replace('weather','').strip()
            print(city_name)
            city_call = get_city_name(city_name)
            if not city_call:
                bot.send_message(chat_id=chat_id,text='Sorry we could not find anything{} \nPlease provide a valid city name'.format(emojize(':slightly_frowning_face:')),reply_to_message_id=reply_message_id)
                return HttpResponse('okay')
            lat, lon = get_lat_lon(city_call)
            reply_text2 = get_weather_details(lat, lon)
            reply_text = reply_weather_info(reply_text2, filename, city_call)        
        if location :
            filename = str(uuid.uuid4())
            lat = body.get('message').get('location').get('latitude')
            longi = body.get('message').get('location').get('longitude')
            reply_text2 = get_weather_details(lat, longi)
            print(reply_text)
            reply_text = reply_weather_info(reply_text2, filename)
            
    except Exception as e:
        print(traceback.format_exc())
        reply_text = "Oops! Something went wrong{} \nPlease try again".format(emojize(':slightly_frowning_face:'))
        return HttpResponse('hi')

    try:
        if location:
            bot.send_photo(chat_id=chat_id, photo=open('{}.png'.format(filename),'rb'))
            try:
                os.remove('{}.png'.format(filename))
            except:
                print('delete operation failed')
        elif 'weather' in text.lower():
            bot.send_photo(chat_id=chat_id, photo=open('{}.png'.format(filename),'rb'))
            try:
                os.remove('{}.png'.format(filename))
            except:
                print('delete operation failed')    
        else:
            bot.send_message(chat_id=chat_id,text=reply_text,parse_mode=telegram.ParseMode.MARKDOWN,reply_to_message_id=reply_message_id)
    
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        reply_text = "Oops! Something went wrong{} \nPlease try again".format(emojize(':slightly_frowning_face:'))
        return HttpResponse('okay')
    
    return HttpResponse("Hi")


def set_webhook(request):
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   print(s)
   if s:
       return HttpResponse("webhook setup ok")
   else:
       return HttpResponse("webhook setup failed")
