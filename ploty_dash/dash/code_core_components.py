import dash
from dash import dcc,html

app = dash.Dash()

app.layout = html.Div([
                    html.Label("Dropdown"),
                    dcc.Dropdown(
                                            id='dropdown',
                                            options=[
                                                {'label': 'Chennai', 'value': 'Chennai'},
                                                {'label': 'Madurai', 'value': 'Madurai'}
                                                ]),
                    html.Label("Slider"),
                    dcc.Slider(
                                id='slider',
                                min=0,
                                max=100,
                                step=10,
                                value=0,
                                marks={i : i for i in range(0,100,10)}),
                    html.P(html.Label("Radiobutton")),
                    dcc.RadioItems(
                                id='radio',
                                options=[
                                    {'label': 'Chennai', 'value': 'Chennai'},
                                    {'label': 'Madurai', 'value': 'Madurai'}
                                ],
                                value='Chennai'
                                )
                    ])
                    

if __name__ == '__main__':
    app.run_server()