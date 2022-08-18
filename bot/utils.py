import json
import datetime
import requests
from PIL import Image, ImageDraw, ImageFont


def get_weather_details(lat, longi):
    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=52897df961304209479a577b6851ca53".format(lat, longi)
    response = requests.request("GET", url)
    print('*********',response.text)
    return response.json()


def get_city_name(city_name):
    url = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid=52897df961304209479a577b6851ca53".format(city_name)
    response = requests.request("GET", url)
    print(response.text)
    return response.json()


def get_lat_lon(data):
    lat = data[0].get('lat')
    lon = data[0].get('lon')
    return lat, lon


def reply_weather_info(data, uuid, city=None):
    place = data.get('name')
    
    if city:
        print(city)
        place = city[0].get('name')
    print(place)
    weather_cond = data.get('weather')[0].get('main')
    temp =  str(data.get('main').get('temp')-273.15)[:4]
    feels_like = str(data.get('main').get('feels_like')-273.15)[:4]
    humidity = str(data.get('main').get('humidity'))
    pressure = str(data.get('main').get('pressure'))
    visibilty = str(data.get('visibility')//1000)
    wind_speed = str(data.get('wind').get('speed'))
    sunrise = str(datetime.datetime.fromtimestamp((data.get('sys').get('sunrise'))))[11:]
    sunset = str(datetime.datetime.fromtimestamp((data.get('sys').get('sunset'))))[11:]
    weather_photo_dict = {'Clear': 'Clearbkg.png', 'Clouds': 'Cloudsbkg.png', 'Drizzle': 'Drizzlebkg.png', 'Fog': 'fogbkg.png', 'Haze': 'Hazebkg.png', 'Mist': 'Mistbkg.png', 'Rain': 'Rainbkg.png', 'Snow': 'Snowbkg.png', 'Storm': 'Stormbkg.png', 'Thunderstorm': 'Thunderstormbkg.png', 'Tornado': 'Tornadobkg.png' }
    filename = weather_photo_dict.get(weather_cond)

    img = Image.open(filename)   
    I1 = ImageDraw.Draw(img)                
    myFont = ImageFont.truetype("corbel.ttf", 20)

    I1.text(xy=(10, 220), text="{}".format(weather_cond), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(10, 180), text="{}".format(place), font=ImageFont.truetype("himalaya.ttf", 40), fill ='navy')
    I1.text(xy=(250, 20), text="Temperature: {}°C".format(temp), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 50), text="Feels Like: {}°C".format(feels_like), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 80), text="Humidity: {} %".format(humidity), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 110), text="Pressure: {} mBar".format(pressure), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 140), text="Visibility: {} km".format(visibilty), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 170), text="Wind Speed: {} km/h".format(wind_speed), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 200), text="Sunrise: {}".format(sunrise), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 230), text="Sunset: {}".format(sunset), font=myFont, fill =(255, 0, 0))

    img.save("{}.png".format(uuid))
    reply_text = img
    
    return reply_text
#

