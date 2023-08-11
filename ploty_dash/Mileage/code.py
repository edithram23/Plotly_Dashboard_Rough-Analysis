import dash
import pandas as pd
import numpy as np
from dash import dcc,html
from dash.dependencies import Output,Input
import plotly.graph_objects as go

app = dash.Dash()

data = pd.read_csv("gapminderDataFiveYear.csv")

app.layout = html.Div([dcc.Graph(id="graph"),
                      
                      dcc.Dropdown(
                        id='year',
                        options=[{'label': str(i), 'value': i} for i in data['year'].unique()],
                        value=data['year'].min()
        )])

@app.callback(Output(component_id="graph",component_property="figure"),
              [Input(component_id="year",component_property="value")])


def update_fig(selected_year):
    
    data_year = data[data["year"]==selected_year]
    
   
    traces = []
    for name in data_year['continent'].unique():
        data_continent = data_year[data_year["continent"]==name]
        traces.append(go.Scatter(x=data_continent["gdpPercap"],y=data_continent["lifeExp"],
                                 name=name,
                                 mode="markers",
                                 marker={'size':15}) )
    print(traces)
    layout = go.Layout(title='Scatterplot',
                       xaxis={'title':"GDP per capita"}, 
                       yaxis={'title':"Life Exp"},
                       )
    
    fig = {'data':traces,'layout':layout}
    return fig


if __name__ == '__main__':
    app.run_server()
    