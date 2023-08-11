import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go

x = np.random.randint(1,101,100)
y = np.random.randint(1,101,100)

data = [go.Scatter(x=x,y=y,mode='markers',
                   marker={'size':12,
                           'color':'#773576',
                           'line':{'width':2}}
                   )]
layout = go.Layout(title="Scatter",xaxis={'title':'x'},yaxis={'title':'y'})
app = dash.Dash()

app.layout = html.Div([dcc.Graph(id="scatterplot",
                                 figure={'data':data,'layout':layout}   
                                ) 
                     ,dcc.Graph(id="ScatterPlot2",
                                 figure={'data':data,'layout':layout}   
                                ) ])

if __name__ == '__main__':
    app.run_server()