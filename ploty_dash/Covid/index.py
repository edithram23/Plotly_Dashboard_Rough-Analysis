import dash
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
from dash import html,dcc
import pycountry
data1 = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'
table = 'https://covid19.who.int/WHO-COVID-19-global-table-data.csv'

try:
    data = pd.read_csv(table,index_col=False)
    data=data[data['Name']!='Other']
    country=data["Name"][1::].unique().tolist()
    NA_LIST = {
        'United States of America': 'USA',
        'Republic of Korea': 'KOR',
        'The United Kingdom': 'GBR',
        'Türkiye': 'TUR',
        'Iran (Islamic Republic of)': 'IRN',
        'Bolivia (Plurinational State of)': 'BOL',
        'occupied Palestinian territory, including east Jerusalem': 'PSE',
        'Republic of Moldova': 'MDA',
        'Venezuela (Bolivarian Republic of)': 'VEN',
        'Kosovo[1]': 'XKX',
        'Democratic Republic of the Congo': 'COD',
        'Côte d’Ivoire': 'CIV',
        'United Republic of Tanzania': 'TZA',
        'Micronesia (Federated States of)': 'FSM',
        'United States Virgin Islands': 'VIR',
        'Northern Mariana Islands (Commonwealth of the)': 'MNP',
        'Saint Martin': 'MAF',
        'Sint Maarten': 'SXM',
        'Bonaire': 'BES',
        'British Virgin Islands': 'VGB',
        'Sint Eustatius': 'BES',
        'Saba': 'BES',
        'Holy See': 'VAT',
        'Pitcairn Islands': 'PCN',
        "Democratic People's Republic of Korea": 'PRK',
    }
    ISO=[' ']
    for country_name in country:
        try:
            country = pycountry.countries.get(name=country_name)
            ISO.append(country.alpha_3)
        except Exception as e:
            
            ISO.append(NA_LIST[country_name])
    data["ISO"]=ISO    
        
    data.to_csv('Dataset/dataset.csv',index=False)        
except:
    print(1)
    data = pd.read_csv('Dataset/dataset.csv')

try:
    data2 = pd.read_csv(data1)
    data2.to_csv('Dataset/dataset2.csv',index=False)
except:
    data2=pd.read_csv('Dataset/dataset2.csv')
global_cases = data[data['Name']=='Global']['Cases - cumulative total'].values[0]
global_cases_new = data[data['Name']=='Global']['Cases - newly reported in last 7 days'].values[0]
global_death = data[data['Name']=='Global']['Deaths - cumulative total'].values[0]
global_death_new = data[data['Name']=='Global']['Deaths - newly reported in last 7 days'].values[0]
print(data)
time=data2["Date_reported"].tail(1).values[0]        

def worldmap_graph():
    value = {
                "Population" : "pop",
                "LifeExpectancy" : "lifeExp",
                "GDP_Percapita" : "gdpPercap"
            }
    color = { "pop" : "RdYLBu",
              "lifeExp" : "Plasma",
              "gdpPercap" : 'RdPu'
             }
    value_ranges = [
    (100000, float('inf'), 'rgb(0, 0, 255)'),  # Values greater than or equal to 100,000 will be blue
    (10001, 100000, 'rgb(51, 153, 255)'),     # Values from 10,001 to 100,000 will be light blue
    (1001, 10000, 'rgb(102, 204, 255)'),      # Values from 1,001 to 10,000 will be sky blue
    (101, 1000, 'rgb(153, 204, 255)'),        # Values from 101 to 1,000 will be pale blue
    (1, 100, 'rgb(204, 229, 255)'),           # Values from 1 to 100 will be very light blue
    (0, 0, 'rgb(245, 245, 245)')               # Values equal to 0 will be light gray
    ]

    # Define the colorscale using the value ranges
    colorscale = []
    for val_range in value_ranges:
        colorscale.append([val_range[0] / max(val_range[1], 1), val_range[2]])

    
    
    fig = {
            'data' : [go.Choropleth(locations=data['ISO'][1::],
                                    z=data['Cases - newly reported in last 7 days'][1::],
                                    text=data["Name"][1::],
                                    colorscale="RdPu",
                                    autocolorscale=False,
                                    reversescale=True,
                                    marker_line_color="darkgray",
                                    marker_line_width=0.5,
                                    showscale=False,
                                    
                                    )],
            'layout': go.Layout(title_text="Life Exp",
                                geo=dict(
                                    showframe=False,
                                    showcoastlines=False,
                                    projection_type="equirectangular",
                                 bgcolor="rgba(0,0,0,0)",
                                    
                                    
                                ),
                                margin = dict(l=0, r=0, b=1, t=0),
                                
                            
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                
                                )
             }    
    return fig



app = dash.Dash(__name__)

app.layout = html.Div([
                        html.Div([
                            html.Div([
                                        html.Img(src=app.get_asset_url('covid_19.PNG'),id='corona',
                                                 style={'height':'60px',
                                                        'width':'auto',
                                                        'margin-bottom':'25px',
                                                        'background-color':'white',
                                                        'padding':'5px'})
                                    ],className="one-third column"),
                            
                            html.Div([
                                        html.Div([
                                            html.H3('CORONAVIRUS')
                                                  ],style={'color':"white",'margin-left':'-250px'})
                                    ],className="one-half column",id="title"),
                            
                            html.Div([
                                        html.Div([
                                                    html.H5('Last Updated :'+time,style={'color':'orange'}),
                                                    
                                                    
                                                ],style={'display':'flex',
                                                         'flex-direction':'row',
                                                         'margin-left':'-20px'})
                                    ]),
                            
                            
                        ],id='header',className='row flex_display',style = {"margin-bottom":'25px'}),
                        
                         html.Div([
                                    html.Div([dcc.Graph(figure=worldmap_graph(),style={"width":"100%",
                                                                             "height":"100%",
                                                                             'padding':'0px'}),
                                            ],className="container nine columns",
                                                style={'margin-top': '50px',
                                                        'margin-bottom': '10px',
                                                       'background-color': 'rgba(0,0,0,0)',
                                                        "position": "relative",
                                                        "left": "50%",
                                                        "transform": "translateX(-50%)",
                                                        "border":"0px",
                                                        "border":"0px rgba(0,0,0,0)",
                                                        'padding':'0px'
                                                        }
                                                )
                                    ]),
                        
                        html.Div([
                                    html.Div([
                                        html.H6('Global cases',style={"text-align":'center',
                                                                      'color':'white',
                                                                      'fontSize':20}),
                                        html.H6(f"{global_cases:,.0f}",
                                                                style={"text-align":'center',
                                                                      'color':'orange',
                                                                      'fontSize':40}),
                                        html.H6("Past 7 days : "+f"{global_cases_new:,.0f}",
                                                                style={"text-align":'center',
                                                                      'color':'orange',
                                                                      'fontSize':10}),
                                        
                                    ],className="card_container three columns"),
                                    
                                    html.Div([html.H6('Global Deaths',style={"text-align":'center',
                                                                      'color':'white',
                                                                      'fontSize':20}),
                                              html.H6(f"{global_death:,.0f}",
                                                                style={"text-align":'center',
                                                                      'color':'red',
                                                                      'fontSize':40}),
                                              html.H6("Past 7 days : "+f"{global_death_new:,.0f}",
                                                                style={"text-align":'center',
                                                                      'color':'red',
                                                                      'fontSize':10})
                                        
                                    ],className="card_container three columns"),
                                    
                                    html.Div([html.H6('Global cases',style={"text-align":'center',
                                                                      'color':'white',
                                                                      'fontSize':20}),
                                              html.H6(f"{global_cases:,.0f}",
                                                                style={"text-align":'center',
                                                                      'color':'green',
                                                                      'fontSize':40})
                                        
                                        
                                    ],className="card_container three columns")
                                    
                            ],className="row flex_display",style={"display":'flex',
                                                                  'flex-direction':'row',
                                                                  'justify-content': 'center',
                                                                  'align-items':'center',
                                                                  'column-gap':'100px'}),
                        
                        html.Div([

                            html.H6("Globally, as of "+time+", there have been "+f"{global_cases:,.0f}"+" confirmed cases of COVID-19",
                                    style={'color':'white',
                                           'fontSize':30,
                                           'font-family':'Playfair Display'
                                          })
                                
                        ],style={"display":'flex',
                                 'flex-direction':'row',
                                 'align-items':'center',
                                 'justify-content': 'center',
                                 'margin-top':40
                                 })
                        
                     ],id="mainContainer",style={"display":'flex',
                                                 'flex-direction':'column'})

################################################################################################






if __name__ == '__main__':
    app.run_server(debug=True)