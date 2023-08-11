import dash
import pandas as pd
from dash import dcc,html
import dash.dependencies
from dash.dependencies import Input,Output,State
from openweather import get_weatherinfo
from geonamescache import GeonamesCache

geonames_case = GeonamesCache()
def cities(country_code='IN'):
    city = geonames_case.get_cities()
    cities_available = [i['name'] for i in city.values() if i['countrycode']==country_code]
    
    return cities_available


data = pd.read_csv("countries.csv")
weather={}
hourly={}
weather,hourly = get_weatherinfo()
image_dict = {
    'Clear': {
        'day': 'sun.gif',
        'night': 'night.gif'
    },
    'Clouds': {
        'day': 'cloudy-day.gif',
        'night': 'cloudy-night.gif'
    },
    'Rain': {
        'day': 'rain.gif',
        'night': 'rain.gif'
    },
    'Thunderstorm': {
        'day': 'thunder-storm.gif',
        'night': 'thunder-storm.gif'
    },
    'Drizzle': {
        'day': 'rain-cloudy-day.gif',
        'night': 'rain.gif'
    },
    'Snow': {
        'day': 'hailstone.gif',
        'night': 'hailstone.gif'
    },
    'Mist': {
        'day': 'foggy.gif',
        'night': 'foggy.gif'
    },
    'Haze': {
        'day': 'haze.gif',
        'night': 'haze.gif'
    },
}



metatags = [{'name': 'viewport',
             'content': 'width=device-width , initial-scale=1.0 , maximum-scale=1.0 , minimum-scale=0.5'}]
app = dash.Dash(__name__,meta_tags=metatags)

app.layout = html.Div([
                        html.Div([
                                   dcc.Interval(id="update",interval=30000000,n_intervals=0),    
                                  html.Div([
                                            html.Div([
                                                        
                                                        html.Div('Weather',className="heading")
                                                     ],className="title_image"),
                                            
                                            html.Div([
                                                       html.Div(id="Time",children=weather['date_time'])
                                            ],className="time")                   
                                        ],className="title twelve columns"),
                                
                                html.Div([
                                    html.Div([dcc.Dropdown(id="continent",
                                                                  options=[{'label':str(data['Country_name'][i])+","+str(data['ISO'][i]),'value':str(data['ISO'][i])} for i in range(len(data))],
                                                                  value='IN')
                                               ],className="dropdown three columns"),
                                           
                                    html.Div([
                                                dcc.Dropdown(id="country",
                                                                 options=[{'label':i,'value':i} for i in cities("IN")],
                                                                  value="Chennai"
                                                             )
                                           ],className="dropdown three columns") 
                                    
                                    ],className="dropdownboxparent"
                                                    ),  

                                
                                html.Div([
                                    html.Div([
                                            
                                            html.Div([
                                                      html.Div(html.Img(id="weather_image",className="weather_image"),className="weather_dabbha"),
                                                      html.Div(id="temp",className="temp"),
                                                      html.Div(id="Location",className="location_time"),
                                                      html.Div(id="Date",className="location_time",style={"margin-top":"10px"})
                                                    ],className="temp_imge"),
                                            
                                            html.Div([
                                                        html.Div([
                                                                
                                                                html.Div(id="description",className="description"),
                                                                html.Div(id="sunrise"),
                                                                html.Div(id="sunset"),
                                                                html.Div(id="humidity"),
                                                                html.Div(id="rain"),
                                                                ],className="weather_desc"),
                                                        html.Div([
                                                                html.Div([
                                                                                html.Div([
                                                                                            html.Div([html.Div(id="wh_hour1"),(html.Img(id="hour1_img",className="icon")),html.Div(id="hour1_txt")],className="weathers_hours")
                                                                                    ]),
                                                                                html.Div([
                                                                                            html.Div([html.Div(id="wh_hour2"),(html.Img(id="hour2_img",className="icon")),html.Div(id="hour2_txt")],className="weathers_hours")
                                                                                    ]),
                                                                                html.Div([
                                                                                            html.Div([html.Div(id="wh_hour3"),(html.Img(id="hour3_img",className="icon")),html.Div(id="hour3_txt")],className="weathers_hours")
                                                                                    ]),
                                                                                html.Div([
                                                                                            html.Div([html.Div(id="wh_hour4"),(html.Img(id="hour4_img",className="icon")),html.Div(id="hour4_txt")],className="weathers_hours")
                                                                                ])
                                                                        ],className="hourly ")
                                                                ],className="content2 ")  
                                                    ],className="desc")  
                                                      
                                            
                                        ],className="dabbha seven columns",style={
                                                                                   }) 
                                    ],className="content")
                                  
                              ],className="row",style={'display':'flex',
                                                        'flex-direction':'column'})
                        
                     ])


#################################################################################################################################################################################
#################################################################################################################################################################################
@app.callback(Output("country","options"),[Input("continent","value")])

def country_name (name):
    return [{'label':i,'value':i} for i in cities(name)]

#################################################################################################################################################################################

#callback

@app.callback(Output("Time","children"),Output("weather_image","src"),Output("temp","children"),
              Output("Date","children"),Output("Location","children"),Output("description","children"),
              Output("sunrise","children"),Output("sunset","children"),Output("humidity","children"),
              Output('hour1_img','src'),Output('hour1_txt','children'),Output('wh_hour1','children'),
              Output('hour2_img','src'),Output('hour2_txt','children'),Output('wh_hour2','children'),
              Output('hour3_img','src'),Output('hour3_txt','children'),Output('wh_hour3','children'),
              Output('hour4_img','src'),Output('hour4_txt','children'),Output('wh_hour4','children'),
              [Input("update",'n_intervals'),Input('country','value')])
def curr_time(n_intervals,city):
    global weather 
    print(city)
    weather,hourly = get_weatherinfo(city)
    #print(weather)
    stats = weather['description']
    icon = image_dict[stats][weather['day/night']]    
    tem=str(int(weather['temperature']))+'°C'    
    
    x = {'icon':{},'temp':{},'time':{}}
    
    for i in range(1,5):
        day = 'night'
        reception_time=int(hourly[i]['time'][0:2]) 
        if( int(reception_time) >=6 and int(reception_time)<18 ):
              day='day'
        stats = hourly[i]['status']
        icon = image_dict[stats][day]
        t=str(int(hourly[i]['temperature']))+'°C' 
        time_i = hourly[i]['time']
        x['icon'][i],x['temp'][i],x['time'][i]=icon,t,time_i
    
        
    
    
    return weather['date_time'],app.get_asset_url(icon),tem,weather['date_time'][0:13],city,"Currently its "+tem+" with "+weather['detailed_status'],"Sunrises :"+weather['sunrise_time'],"Sunsets :"+weather['sunset_time'],"Humidity :"+str(weather['humidity'])+"%",app.get_asset_url(x['icon'][1]),x['temp'][1],x['time'][1],app.get_asset_url(x['icon'][2]),x['temp'][2],x['time'][2],app.get_asset_url(x['icon'][3]),x['temp'][3],x['time'][3],app.get_asset_url(x['icon'][4]),x['temp'][4],x['time'][4]


    
if __name__ == '__main__':
    app.run()