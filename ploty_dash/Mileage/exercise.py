import dash
from dash.dependencies import Input,Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import html,dcc 


app = dash.Dash()


app.layout = html.Div([html.Div("RANGE Slider"),
                       dcc.RangeSlider(
                                        id='slider',
                                        min=0,
                                        max=100,
                                        step=10,
                                        value=[0, 100]),
                       html.Div(id="selected_range")
                       ])

@app.callback(Output("selected_range","children"),[Input("slider","value")])

def selected_range(range):
    print(range)
    return "Your selected range {}".format(range[0]*range[1])
                      
if __name__ == '__main__':
    app.run_server()                      