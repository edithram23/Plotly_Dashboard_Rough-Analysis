import dash 
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc
from dash import html
app = dash.Dash() 

bg = '#111111'
text = '#FFFFFF'

app.layout = html.Div(children=[
                                html.H1("Hello World!",style={'textAlign':'center','color':text}),
                                dcc.Graph(id='23',
                                          figure={
                                                    'data' : [
                                                                {"x" : [1,2,3] , 'y' : [4,1,2] , 'type' : 'bar' , 'name': 'A'},
                                                                {"x" : [1,2,3] , 'y' : [41,2,5] , 'type' : 'bar' , 'name': 'B'}
                                                    ],
                                                     'layout' : {'title' :"Box plot in Dash",
                                                                  'plot_bgcolor' : bg ,
                                                                  'paper_bgcolor' : bg,
                                                                  'font' : {"color":text}
                                                                      
                                                                 }
                                                      
                                                }
                                          )   
                                ],style={'backgroundColor':bg}
                      )

if __name__ == '__main__':
    app.run_server()
        