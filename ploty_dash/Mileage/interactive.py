import dash 
import pandas as pd
import numpy as np
from dash import html,dcc
from dash.dependencies import Input,Output,State
import base64
import json
import plotly.graph_objects as go

app = dash.Dash()

def encode_img (img_file):
    encoded = base64.b64encode(open(img_file,'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())

data = pd.read_csv ("wheels.csv")

df = [go.Scatter(x=data["color"],y=data["wheels"],dy=1,mode="markers" )]
layout = go.Layout(title="Scatterplot",
                   xaxis=dict(title="Color"),
                   yaxis=dict(title="Wheels"),
                   hovermode = 'closest'
                   )
fig = {'data': df, 'layout': layout}




app.layout = html.Div([html.Div([dcc.Graph(id="plot",figure=fig)]),
                       html.Div([html.Hr()]),
                       html.Div(id="Text",style={'font-size':15,
                                                 'font-family':'Times New Roman',
                                                 'bold': True}),
                       html.Div([html.Img(id = "hover_data",src='children',height=300)],
                      style={'padding':'35'})
                      ])
@app.callback(Output("hover_data","src"),
              [Input("plot","clickData")])

def output_hover_data(hoverData):
    #print(hoverData)
    wheel = hoverData['points'][0]['y']
    color = hoverData['points'][0]['x']
   # print(wheel, color)
    path = 'E:/SNU/ploty_dash/plotlydash/images/'
    print(path+data[(data['wheels']==wheel) & (data['color']==color) ]['image'].values[0])
    return encode_img(path+data[(data['wheels']==wheel) & (data['color']==color) ]['image'].values[0])

@app.callback(Output("Text","children"),
              [Input("plot","clickData")])

def output_text(hoverData):
    wheel = hoverData['points'][0]['y']
    color = hoverData['points'][0]['x']
    return str(wheel) + ' ' + color 
if __name__ == "__main__":
    app.run_server()