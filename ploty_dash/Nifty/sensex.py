import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from datetime import date, datetime

app = dash.Dash()

data = pd.read_csv("Nifty_200_scripts.csv")
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
print(data)
bg = '#000000'
text = '#FFFFFF'

app.layout = html.Div(
    style={'backgroundColor': 'black', 'color': text, 'border':'black', 'padding': 'black', 'width': '100%', 'height': '100%'},
    children=[
        html.Div(
            "Nifty_200_scripts",
            style={"fontSize": "24px"}
        ),
        html.Br(),
        html.Div(
            style={ 'backgroundColor': bg, 'borderRadius': '10px'},
            children=[
                html.Div(
                    style={'width': '50%', 'padding': '20px'},
                    children=[
                        html.Table(
                            style={'width': '100%', 'textAlign': 'left', 'color': text},
                            children=[
                                html.Tr([
                                    html.Th("Select a Stock Symbol"),
                                    html.Th("Select Date range")
                                ]),
                                html.Tr([
                                    html.Td([
                                        dcc.Dropdown(
                                            id="stock_name",
                                            options=[{'label': i, 'value': i} for i in data["Symbol"].unique()],
                                            value=data["Symbol"][0],
                                            style={"width": "100%", "color": bg, "backgroundColor": text}
                                        )
                                    ]),
                                    html.Td([
                                        dcc.DatePickerRange(
                                            id="date_picker",
                                            min_date_allowed=data["Date"].min(),
                                            max_date_allowed=data["Date"].max(),
                                            
                                            
                                            style={"color": text, "backgroundColor": bg}
                                        )
                                    ]),
                                    html.Td([
                                        html.Button(
                                            children="Submit",
                                            id="submit",
                                            style={
                                                "marginLeft": "20%",
                                                "color": bg,
                                                "backgroundColor": "#FFFFFF",
                                                "border": "none",
                                                "padding": "10px 20px",
                                                "borderRadius": "5px",
                                                "cursor": "pointer"
                                            },
                                            n_clicks=0
                                        )
                                    ], style={"marginLeft": "20%"})
                                ])
                            ]
                        )
                    ]
                ),
                html.Div(
                    id="stock_info",
                    style={'width': '50%', 'padding': '20px'}
                )
            ]
        ),
        html.Br(),
        html.Div([
            dcc.Graph(
                id="plot",
                figure={
                    'data': [],
                    'layout': {
                        'plot_bgcolor': bg,
                        'paper_bgcolor': bg,
                        'font': {'color': text},
                        'title': {'text': 'Stock Prices', 'font': {'size': '24px', 'color': text}},
                        'xaxis': {'title': 'Date', 'color': text},
                        'yaxis': {'title': 'Price', 'color': text}
                    }
                }
            )
        ])
    ]
)

@app.callback(Output("date_picker","min_date_allowed"),Output("date_picker","max_date_allowed"),Output("date_picker","start_date"),Output("date_picker","end_date"),
              [Input("stock_name","value")])
def update(name):
    if name is None: 
        return None, None,None,None
    x=data[data["Symbol"] == name]["Date"].min()
    y=data[data["Symbol"] == name]["Date"].max()

    x=x.strftime("%Y-%m-%d")
    y=y.strftime("%Y-%m-%d")                    
    print(x, y)
    return x,y,x,y

@app.callback(
    Output("plot", "figure"),
    [Input("submit", "n_clicks")],
    [
        State('stock_name', 'value'),
        State("date_picker", "start_date"),
        State("date_picker", "end_date")
    ]
)

def graph(clicks, name, start, end):
    if start is None or end is None:
        return {'data': [], 'layout': {
            'plot_bgcolor': bg,
            'paper_bgcolor': bg,
            'font': {'color': text},
            'title': {'text': 'Stock Prices', 'font': {'size': '24px', 'color': text}},
            'xaxis': {'title': 'Date', 'color': text},
            'yaxis': {'title': 'Price', 'color': text}
        }}

    x = datetime.strptime(start, "%Y-%m-%d")
    y = datetime.strptime(end, "%Y-%m-%d")
    x = x.strftime("%d-%m-%Y")
    y = y.strftime("%d-%m-%Y")
    start_date, end_date = x, y
    print(start_date, end_date)
    print(data[data["Symbol"]==name])
    df = data[(data['Symbol'] == name) & (data['Date'].between(start_date, end_date))]
    print(df)

    # If no data is available for the selected date range
    if df.empty:
        return {'data': [], 'layout': {
            'plot_bgcolor': bg,
            'paper_bgcolor': bg,
            'font': {'color': text},
            'title': {'text': 'No Data Available', 'font': {'size': '24px', 'color': text}},
            'xaxis': {'title': 'Date', 'color': text},
            'yaxis': {'title': 'Price', 'color': text}
        }}
    print(df)
    trace = []
    trace1 = go.Scatter(x=df['Date'], y=df["Open"], mode="lines+markers", line={'color': '#FFFFFF'})
    layout = go.Layout(title="Nifty2020")
    return {'data': [trace1], 'layout': {
        'title':"Nifty"+" "+name,
        'plot_bgcolor': bg,
        'paper_bgcolor': bg,
        'font': {'color': text},
        'title': {'text': 'Stock Prices', 'font': {'size': '24px', 'color': text}},
        'xaxis': {'title': 'Date', 'color': text},
        'yaxis': {'title': 'Price', 'color': text},
        "tickformat":"%b %Y",
        "tickfont":dict(color=text),
        "hoverformat":"%b %Y"
    }}



@app.callback(
    Output("stock_info", "children"),
    [Input("plot", "hoverData")],
    [State('stock_name', 'value')]
)
def display_stock_info(hover_data, stock_name):
    if hover_data is None:
        return []
    x_val = hover_data["points"][0]["x"]
    stock_data = data[(data['Symbol'] == stock_name) & (data['Date'] == x_val)]
    
    
    high = stock_data['High'].values[0]
    low = stock_data['Low'].values[0]
    open_val = stock_data['Open'].values[0]
    close = stock_data['Close'].values[0]
    info_table = html.Table(
        style={'width': '100%', 'textAlign': 'left', 'color': text},
        children=[
            html.Tr([html.Th("Stock Information", colSpan="2")]),
            html.Tr([html.Td("High"), html.Td(high)]),
            html.Tr([html.Td("Low"), html.Td(low)]),
            html.Tr([html.Td("Open"), html.Td(open_val)]),
            html.Tr([html.Td("Close"), html.Td(close)]),
        ]
    )
    return [info_table]


if __name__ == '__main__':
    app.run_server()
