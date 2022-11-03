import datetime
import requests
from PIL import ImageDraw, ImageFont
from PIL import Image
import pytz


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


'''[{"name":"Delhi","local_names":{"lv":"Deli","el":"Δελχί","he":"דלהי","de":"Delhi","kn":"ದೆಹಲಿ","ms":"Delhi","ar":"دلهي","te":"ఢిల్లీ","hi":"दिल्ली","ne":"दिल्ली","ml":"ഡെൽഹി","bn":"দিল
্লি","ur":"دہلی","ta":"தில்லி","ja":"デリー","ko":"델리","en":"Delhi","cs":"Dillí","uk":"Делі","es":"Delhi","my":"ဒေလီမြို့","zh":"德里","ku":"Delhî","ru":"Дели","th":"เดลี","eo":"Delh
io","oc":"Delhi","pa":"ਦਿੱਲੀ","fr":"Delhi","fa":"دهلی","pt":"Deli"},"lat":28.6517178,"lon":77.2219388,"country":"IN","state":"Delhi"}]'''


def get_lat_lon(data):
    lat = data[0].get('lat')
    lon = data[0].get('lon')
    return lat, lon


''' {"coord":{"lon":77.2219,"lat":28.6517},
"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04n"}],
"base":"stations","main":{"temp":304.44,"feels_like":310.6,"temp_min":304.44,"temp_max":304.44,"pressure":998,"humidity":67,"sea_level":998,"grnd_level":974},
"visibility":10000,"wind":{"speed":3.83,"deg":46,"gust":7.85},"clouds":{"all":100},"dt":1660226603,
"sys":{"type":2,"id":2011697,"country":"IN","sunrise":1660177078,"sunset":1660224895},"timezone":19800,"id":1273840,"name":"Connaught Place","cod":200}'''


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
    sunrise = (datetime.datetime.fromtimestamp((data.get('sys').get('sunrise'))))
    sunrise_ist = sunrise.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S')
    sunset = (datetime.datetime.fromtimestamp((data.get('sys').get('sunset'))))
    sunset_ist = sunset.astimezone(pytz.timezone('Asia/Kolkata')).strftime('%H:%M:%S')
    weather_photo_dict = {'Clear': 'Clearbkg.png', 'Clouds': 'Cloudsbkg.png', 'Drizzle': 'Drizzlebkg.png', 'Fog': 'Fogbkg.png', 'Haze': 'Hazebkg.png', 'Mist': 'Mistbkg.png', 'Rain': 'Rainbkg.png', 'Snow': 'Snowbkg.png', 'Storm': 'Stormbkg.png', 'Thunderstorm': 'Thunderstormbkg.png', 'Tornado': 'Tornadobkg.png', 'Smoke': 'smokebkg.png' }
    filename = weather_photo_dict.get(weather_cond)

    img = Image.open(filename)   
    I1 = ImageDraw.Draw(img)                
    myFont = ImageFont.truetype("CORBEL.TTF", 20)

    I1.text(xy=(10, 220), text="{}".format(weather_cond), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(10, 190), text="{}".format(place), font=ImageFont.truetype("Himalaya Regular.ttf", 20), fill ='navy')
    I1.text(xy=(250, 20), text="Temperature: {}°C".format(temp), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 50), text="Feels Like: {}°C".format(feels_like), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 80), text="Humidity: {} %".format(humidity), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 110), text="Pressure: {} mBar".format(pressure), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 140), text="Visibility: {} km".format(visibilty), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 170), text="Wind Speed: {} km/h".format(wind_speed), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 200), text="Sunrise: {}".format(sunrise_ist), font=myFont, fill =(255, 0, 0))
    I1.text(xy=(250, 230), text="Sunset: {}".format(sunset_ist), font=myFont, fill =(255, 0, 0))

    img.save("{}.png".format(uuid))
    reply_text = img
    
    return reply_text
#

