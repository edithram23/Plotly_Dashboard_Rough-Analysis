from pyowm.owm import OWM
import requests
import datetime 
import pytz

def get_weatherinfo(city="Thanjavur"):
    owm = OWM('9a6fcd868d3b81a80299f7e2d0b88124')
    mgr = owm.weather_manager()
    weather1 = mgr.weather_at_place(city)
    weather = weather1.weather
    
   
  
    
    temperature = weather.temperature('celsius')['temp']
    humidity = weather.humidity
    wind_speed = weather.wind()['speed']
    description = weather.status
    cloud_coverage = weather.clouds
    atmospheric_pressure = weather.pressure['press']
    sunrise_time = weather.sunrise_time(timeformat='date')
    sunset_time = weather.sunset_time(timeformat='date')
    weather_icon_url = weather.weather_icon_url(size='2x')
    detailed_status = weather.detailed_status
    reception_time = weather1.reception_time()
    reception_time = datetime.datetime.fromtimestamp(reception_time)

    # weather_rain = weather.rain
    # print(weather_rain)
    
    forecast = mgr.forecast_at_place(city,'3h')
    hourly_forecast = {}
    count=0
    for data in forecast.forecast:
        if(count==4):
            break
        count+=1
        time = data.reference_time('date')
        ist_timezone = pytz.timezone('Asia/Kolkata')
        ist_time = time.astimezone(ist_timezone)
        time = ist_time.strftime("%H:%M")
    
        tem = data.temperature('celsius')['temp']
        humid = data.humidity
        des = data.status
        rain = data.rain
        if (rain=={}):
            rain['3h']=0
        hourly_forecast[count] = {'time':time,'temperature':tem, 'humidity':humid,'status':des,'rain':rain}
        
    day = 'night'
    if( int(reception_time.strftime("%H")) >=6 and int(reception_time.strftime("%H"))<18 ):
        day='day'
    reception_time = "{} {}" .format(reception_time.strftime("%B %d, %Y"),reception_time.strftime("%H:%M:%S"))
    
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_time = sunrise_time.astimezone(ist_timezone)
    sunrise_time = ist_time.strftime("%dth %B %H:%M")
        
    ist_timezone = pytz.timezone('Asia/Kolkata')
    ist_time = sunset_time.astimezone(ist_timezone)
    sunset_time = ist_time.strftime("%dth %B %H:%M")
    
    response = requests.get(weather_icon_url)
    icon_filename = 'assets/weather_icon.png'
    with open(icon_filename, 'wb') as file:
        file.write(response.content)
    climate_weather ={
    "date_time":reception_time,    
    "temperature": temperature,
    "humidity": humidity,
    "wind_speed": wind_speed,
    "description": description,
    "cloud_coverage": cloud_coverage,
    "atmospheric_pressure": atmospheric_pressure,
    "sunrise_time": sunrise_time,
    "sunset_time": sunset_time,
    "weather_icon_url": weather_icon_url,
    "detailed_status": detailed_status,
    "day/night": day
    # "rain":weather_rain
    }
    return climate_weather,hourly_forecast

  
 