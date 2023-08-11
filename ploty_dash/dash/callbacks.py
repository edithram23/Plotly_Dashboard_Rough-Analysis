import dash 
from dash import dcc,html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
app = dash.Dash()

app.layout = html.Div([
                       dcc.Input(id="dash1",value="Enter",type="text"),
                       html.Div(id="dash2",style={"color":"red"})
                      ])

@app.callback(Output(component_id="dash2",component_property="children"),
              [Input(component_id="dash1",component_property="value")])
def input_output(input_value):
    return "You Entered {}".format(input_value)


if __name__ == "__main__":
    app.run_server()