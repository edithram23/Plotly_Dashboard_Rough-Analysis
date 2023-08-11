import dash
import pandas as pd
from dash.dependencies import Output,Input
import plotly.graph_objects as go
from dash import html,dcc
import numpy as np


app = dash.Dash()

data = pd.read_csv("mpg.csv")

df = [go.Scatter(x=data["model_year"],y=data["mpg"],
                 text=data['name'],
                 hoverinfo=['text','y','x'],
                 mode="markers"
                )]

layout = go.Layout(title="Scatter plot",
                   xaxis=dict(title="model year"),
                   yaxis=dict(title="mpg"),
                   hovermode='closest'
                   )

fig = {'data':df,'layout':layout}

app.layout = html.Div([html.Div(),
                       html.Div([
                                dcc.Graph(id="graph",figure= fig)
                                ],style={'width':"50%","display":"inline-block"})
                       ])


if __name__ == '__main__':
    app.run_server()
 