import pandas as pd
import numpy as np
import dash 
from dash import html,dcc
import plotly.graph_objects as go

app = dash.Dash()

data = pd.read_csv("OldFaithful.csv")
data.info()
data.head(20)

df = [go.Scatter(x=data["X"], y=data["Y"],name=date,mode="markers") for date in data["D"] ]

layout = go.Layout(title="OldFaithful")

app.layout = html.Div([dcc.Graph(id="Scp",
                                 figure={"data":df , "layout":layout , "title":"X vs Y "})])

if __name__ == '__main__':
    app.run_server()