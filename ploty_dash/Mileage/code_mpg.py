import dash 
from dash import dcc,html
from dash.dependencies import Input,Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

app = dash.Dash()

data = pd.read_csv("mpg.csv")
columns = data.columns

app.layout = html.Div([
                        html.Div([
                                    dcc.Dropdown(id="x_axis",
                                    options=[{'label':column , 'value':column}for column in columns],
                                    value=columns[1])
                                 ],style={'width':'48%' ,'display' :'inline-block'}),
                        html.Div([dcc.Dropdown(id="y_axis",
                                               options=[{'label':column , 'value':column}for column in columns],
                                               value=columns[1])
                                  ],style={'width':'48%' ,'display' :'inline-block'}),
                        dcc.Graph(id="graph")
                        
                     ],style={'padding':10})

@app.callback(Output(component_id="graph",component_property="figure"),
              [Input(component_id="x_axis",component_property="value"),
               Input(component_id="y_axis",component_property="value")])

def output_graph(x_in,y_in):
    
    traces = [go.Scatter(x=data[x_in],y=data[y_in],
                         mode='markers',
                         text=data["name"],
                         marker={'size':15,
                                 'opacity':0.5,
                                 'line':{'width':0.5,'color':'white'}},
                         )]
    
    layout = go.Layout(title="{} {}".format(x_in,y_in),
                       xaxis=dict(title=x_in),
                       yaxis=dict(title=y_in),
                       hovermode="closest"
                       )
    
    
    fig = {'data':traces,'layout':layout}
    return fig


if __name__=='__main__':
    app.run_server()