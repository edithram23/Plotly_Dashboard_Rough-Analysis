import pandas as pd
import numpy as np
import dash
from dash import html,dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go


data = pd.read_csv("JupyterNotebook/updated.csv")
continent=data["continent"].unique().tolist()
ISO = data["ISO"].unique().tolist()
##########################################################################################################################################################################################################################################

meta_tags =[{'name':'viewport','content':'width-device'}]
app = dash.Dash(__name__,meta_tags=meta_tags)

def function1(continent,values):
    data1 = data[data["year"]==2007]
    data2 = data1[data1["continent"]==continent]
    data2 = data2.sort_values(by=values,ascending=False)
    data2 = data2[0:10]
    print(continent,values)
    return data2.reset_index()



app.layout = html.Div([
                        html.Div([
                            
                                html.Div([ 
                                          #Heading
                                            html.H6('World Countries Information',className='title_text')],className="title_container twelve columns")
                                ],className="row flex_display"),
                        
                        html.Div([
                                    html.Div([dcc.Dropdown(id="continent",
                                                                  options=[{'label':i,'value':i} for i in continent],
                                                                  value=continent[0])
                                               ],className="dropdown three columns"),
                                           
                                    html.Div([
                                                dcc.Dropdown(id="country")
                                           ],className="dropdown three columns") 
                                    
                                    ],className="dropdownboxparent"
                                                    ),
                                
                        html.Div([
                                    html.Div([dcc.Dropdown(id="graph_value",
                                                                  options=[{'label':i,'value':i} for i in ["Population","LifeExpectancy","GDP_Percapita"]],
                                                                  value="LifeExpectancy",
                                                                  )
                                               ],className="dropdown three columns")
                                ],className="dropdownboxparent",style={
                                                                        'margin-top':'30px'
                                                                      }),    

    
                        html.Div([
                                    html.Div([dcc.Graph(id="worldmap",style={"width":"100%",
                                                                             "height":"100%",
                                                                             'padding':'0px'}),
                                            ],className="container nine columns",
                                                style={'margin-top': '50px',
                                                        'margin-bottom': '10px',
                                                        'background-color': 'rgba(0,0,0,0)',
                                                        "position": "relative",
                                                        "left": "50%",
                                                        "transform": "translateX(-50%)",
                                                        "border":"0px rgba(0,0,0,0)",
                                                        'padding':'0px'
                                                        }
                                                )
                                    
                                    ]),
                            
                        html.Div([
                                    html.Div([
                                                html.Div([
                                                                html.H3(id='box1_heading', className='subheading', children='Trends over the years')
                                                        ]),
                                                html.Div([
                                                    dcc.Graph(id="graph1")
                                                ])
                                                ],className="container six columns",
                                                style={
                                                        'margin-top': '20px',
                                                        'margin-bottom': '10px',
                                                        
                                                }
                                                ),
                                    html.Div([
                                                html.Div([
                                                                html.H3(id='box2_heading', className='subheading', children='Trends over the years')
                                                        ]),
                                                html.Div([
                                                    dcc.Graph(id="graph2")
                                                ])
                                                ],className="container six columns",
                                                style={
                                                        'margin-top': '20px',
                                                        'margin-bottom': '10px',
                                                        
                                                }
                                                ),
                                    ])   
                                    
    
                     ],className="mainContainer",style={'display':'flex',
                                                        'flex-direction':'column'})

##########################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################
##########################################################################################################################################################################################################################################

#callback 1

@app.callback(Output("country","options"),Output("country","value"),
              [Input("continent","value")])

def country_options(continent_name):
    country_options = data[data["continent"]==continent_name]["country"].unique().tolist()
    return  [{'label':i,'value':i} for i in country_options],country_options[0]

##########################################################################################################################################################################################################################################

#callback 2

@app.callback(Output("worldmap","figure"),
              [Input("country","value"),Input("continent","value"),Input("graph_value","value")])

def worldmap_graph(country_name,continent_name,graph_value):
    value = {
                "Population" : "pop",
                "LifeExpectancy" : "lifeExp",
                "GDP_Percapita" : "gdpPercap"
            }
    color = { "pop" : "RdYLBu",
              "lifeExp" : "Plasma",
              "gdpPercap" : 'RdPu'
             }
    fig = {
            'data' : [go.Choropleth(locations=data["ISO"],
                                    z=data[value[graph_value]],
                                    text=data["country"],
                                    colorscale=color[value[graph_value]],
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

##########################################################################################################################################################################################################################################

#callback 3 

@app.callback(Output("graph1","figure"),
              [Input("country","value"),Input("continent","value"),Input("graph_value","value")])
def graph_1(country_name,continent_name,value):
    
    value1 = {
                "Population" : "pop",
                "LifeExpectancy" : "lifeExp",
                "GDP_Percapita" : "gdpPercap"
            }
    
    value = value1[value]
    
    color = { "pop" : "RdYLBu",
              "lifeExp" : "Plasma",
              "gdpPercap" : 'RdPu'
             }
    
    fig= {'data': [go.Scatter(x=data["year"],
                              y=data[data["country"]==country_name][value],
                              mode="lines+markers",
                              name=country_name,
                              
                              opacity=0.8,
                              hoverinfo="x+y"                              
                  )],
          'layout': go.Layout()}    
    return fig

##########################################################################################################################################################################################################################################

#callback 4
@app.callback(Output("graph2","figure"),
              [Input("country","value"),Input("continent","value"),Input("graph_value","value")])
def graph_1(country_name,continent_name,value):
    
    value1 = {
                "Population" : "pop",
                "LifeExpectancy" : "lifeExp",
                "GDP_Percapita" : "gdpPercap"
            }
    
    value = value1[value]
    
    colors = { "pop" : "RdYLBu",
              "lifeExp" : "Plasma",
              "gdpPercap" : 'RdPu'
             }
    
    data1 = function1(continent_name,value)
    print(data1)
    fig = {'data': [go.Bar(x=data1[value],
                           y=data1['country'],
                           marker=dict(colorscale=colors[value],
                                       color=data[value]),
                           orientation='h')  
                   ],
           'layout': go.Layout(
                                coloraxis=dict(
                                    colorbar=dict(
                                        title="Colotbar",
                                        cmin=min(data[value]),
                                        cmax=max(data[value])
                                    )
                                )
           )}
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)