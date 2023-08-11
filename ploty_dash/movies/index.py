import dash
import pandas as pd
from dash import html,dcc
from dash.dependencies import Input,Output
import plotly.graph_objects as go
##########################################################################################################################################################################################################################################


data = pd.read_csv("JupyterNotebook/dataset.csv")
year_data = data["Year"].unique()
year_data = year_data.tolist()


def function1(year,m=None):
    if(m!=None):
        pie = data.groupby(["mpaa_rating","Year"])["total_gross"].sum().reset_index()
        value=pie[pie["Year"]==year]
        features = value["mpaa_rating"].unique().tolist()
        print(features)
        
            
            
        return value,features
    
    table_gross_value = data.groupby(["genre","Year"])["total_gross"].sum().reset_index()
    features = data["genre"].unique().tolist()
    features[6]=0
    features.remove(0)
    value = {x:[table_gross_value[(table_gross_value["genre"]==x) & (table_gross_value["Year"]==year)]["total_gross"],
           ((table_gross_value[(table_gross_value["genre"]==x) & (table_gross_value["Year"]==year)]["total_gross"]/(table_gross_value[table_gross_value["Year"]==year]["total_gross"].sum()))*100)
           ] for x in features }
    for key, val in value.items():
        if val[0].empty:
            val[0] = 0
        if val[1].empty:
            val[1] = 0
    for key,val in value.items():
        val[0]=int(val[0])
        val[1]=float(val[1])
    
        
    return value,features    
        
##########################################################################################################################################################################################################################################


font = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css"

tags = [{'name':'viewport','content':'width-device-width'}]
ex_css = [font,tags]
app = dash.Dash(__name__,external_stylesheets=ex_css)
server = app.server
app.layout = html.Div([
                        
                        html.Div([
                            
                                html.Div([ 
                                          #Heading
                                            html.H5('Movies (1996-2016) Data Analysis',className='title_text')],className="title_container twelve columns")
                                ],className="row flex_display"),
                        html.Div([
                                  html.Div([
                                            #paragraph about the table
                                            html.P([dcc.Markdown(""" **Below Table** shows **Gross Sales Values** for each genre category and percentage 
                                                                 of share for each genre category in each year:""")],style={'line-height':'1',                  # use ** for bold , start and end the text with ** to make it bold
                                                                                                    'font-size':'17px',
                                                                                                    'text-align':'justify',
                                                                                                    'margin-bottom':'20px'}),
                                            
                                            
                                            html.Div(id="table_calculation")
                                      


                                            ],className="container six columns",
                                             style={'margin-top': '10px',
                                                    'margin-bottom': '10px',
                                                    'background-color': 'lavender'
                                                    
                                                    }),
                                  
                                  html.Div([
                                            html.Div([  #Year tag 
                                                        html.P(children="Year",className="label", style={'color':'black'}),
                                                        #Year slider
                                                        dcc.Slider(id="year_selector",
                                                                        min=year_data[0],
                                                                        max=year_data[-1],
                                                                        step=1,
                                                                        value=year_data[6],
                                                                        included=False,
                                                                        updatemode='drag',
                                                                        tooltip={'always': True},
                                                                        marks={str(i):str(i) for i in  range(year_data[0],year_data[-1]+1,2)},
                                                                        className="slider_component"
                                                                        
                                                                        )
                                                    ],className='container_slider')
                                                                         

                                            ],className="container six columns",
                                              style={'margin-top': '10px',
                                                    'margin-bottom': '10px',
                                                    'background-color': 'lavender'
                                                    }),
                                  
                                  html.Div([
                                            
                                            dcc.Graph(id="pie_chart",
                                                        config=dict(displayModeBar='hover'),
                                                        className="piechart",style={'border':"1px solid black"}
                                                        ),

                                            html.P([dcc.Markdown(id="share_year")],
                                                                                            style={'line-height':'1',                  
                                                                                                    'font-size':'17px',
                                                                                                    'text-align':'justify',
                                                                                                    'margin-bottom':'20px',
                                                                                                    'margin-top':'50px'}),
                                            html.Div(id="share_table")            
                                                        
                                                        
                                           ],className="container six columns",style={'background-color': 'lavender',
                                                                                      'margin-top':'40px'}),
                                  
                                  
                                ]),
                        html.Div([
                                 html.Div([
                                            dcc.Graph(id="bar_plot",
                                                               config={'displayModeBar':'hover'},
                                                               className="bar_plot")
                                             
                                           ],className="container six columns",
                                             style={'margin-top': '-380px',
                                                    'margin-bottom': '10px',
                                                    'background-color': 'lavender'})
                                  ])
                                  
                                  
                       
                    ],className="mainContainer",
                        style={'display':'flex','flex-direction':'column'})         #flex is used to bring the webpage to view in a single column,like mobile view



###########################################################################################################################################################################################################################################
###########################################################################################################################################################################################################################################
###########################################################################################################################################################################################################################################

#callback table


@app.callback(Output("table_calculation","children"),
               Input("year_selector","value"))


def table(year):
    
    value,features = function1(year)
    
    
    return [
                html.Table([
                            html.Thead([
                                            html.Tr([
                                                        html.Th('Genre'),
                                                        html.Th("Symbol"),
                                                        html.Th("Gross Sales($) "+str(year)),
                                                        html.Th("% Share "+str(year))
                                                        
                                                        
                                                ],className="TableHeader")
                                      ]),
                            
                            html.Tbody([ 
                                            html.Tr([
                                                        html.Td(features[0]),
                                                        html.Td(html.I(className="fas fa-star",style={"font-size":'18px','text-align':'center'})),
                                                        html.Td(value[features[0]][0]),
                                                        html.Td(round(value[features[0]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[1]),
                                                        html.Td([html.I(className="fas fa-heart",style={"font-size":'18px','text-align':'center'})," ",html.I(className="fas fa-laugh-squint",style={"font-size":'18px'})]),
                                                        html.Td(value[features[1]][0]),
                                                        html.Td(round(value[features[1]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[2]),
                                                        html.Td(html.I(className="fas fa-theater-masks",style={"font-size":'18px','text-align':'center'})),
                                                        html.Td(value[features[2]][0]),
                                                        html.Td(round(value[features[2]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[3]),
                                                        html.Td(html.I(className="fas fa-smile",style={"font-size":'18px','text-align':'center'})),
                                                        html.Td(value[features[3]][0]),
                                                        html.Td(round(value[features[3]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[4]),
                                                        html.Td(html.I(className="fas fa-fist-raised",style={"font-size":'18px'})),
                                                        html.Td(value[features[4]][0]),
                                                        html.Td(round(value[features[4]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[5]),
                                                        html.Td(html.I(className="fas fa-exclamation-triangle",style={"font-size":'18px'})),
                                                        html.Td(value[features[5]][0]),
                                                        html.Td(round(value[features[5]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[6]),
                                                        html.Td(html.I(className="fas fa-music",style={"font-size":'18px'})),
                                                        html.Td(value[features[6]][0]),
                                                        html.Td(round(value[features[6]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[7]),
                                                        html.Td(html.I(className="fas fa-laugh-squint",style={"font-size":'18px'})),
                                                        html.Td(value[features[7]][0]),
                                                        html.Td(round(value[features[7]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[8]),
                                                        html.Td(html.I(className="fas fa-skull-crossbones",style={"font-size":'18px'})),
                                                        html.Td(value[features[8]][0]),
                                                        html.Td(round(value[features[8]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[9]),
                                                        html.Td(html.I(className="fas fa-hat-cowboy",style={"font-size":'18px'})),
                                                        html.Td(value[features[9]][0]),
                                                        html.Td(round(value[features[9]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[10]),
                                                        html.Td(html.I(className="fas fa-file-alt",style={"font-size":'18px'})),
                                                        html.Td(value[features[10]][0]),
                                                        html.Td(round(value[features[10]][1],3))
                                            ],className="table_row"),
                                            html.Tr([
                                                        html.Td(features[11]),
                                                        html.Td(html.I(className="fas fa-microphone",style={"font-size":'18px'})),
                                                        html.Td(value[features[11]][0]),
                                                        html.Td(round(value[features[11]][1],3))
                                            ],className="table_row")
                                            
                                        ])
                            ],className="table")
    ]

###########################################################################################################################################################################################################################################

#callback bar_plot

@app.callback(Output("bar_plot","figure"),
              [Input("year_selector",'value')])

def bar_plot_graph(year):
    
    value,features= function1(year)
    y_value = []
    for key,val in value.items():
         y_value+=[val[0]]
         
    hovertext = [f'<b>Year</b>: {year}<br><b>Gross Sales</b>: {x:,.0f}<br>' for x in y_value]   
    fig = {'data':  [go.Bar(x=features,y=y_value,
                            text=y_value,
                            texttemplate='%{text:,.2s}',
                            textposition='outside',
                            marker=dict(color='rgb(178, 117, 236)'),
                            textfont=dict(family="Roboto",
                                          size=12,
                                          color='black'),
                            hoverinfo='text',
                            hovertext=hovertext
                            )],
           'layout': go.Layout(plot_bgcolor= 'white',
                               paper_bgcolor= 'white',
                               title=dict(text="Gross Sales "+str(year),
                                          y=0.98,
                                          x=0.5,
                                          xanchor='center',
                                          yanchor='top'
                                          ),
                               titlefont=dict(color="black",
                                              size=17),
                               hovermode="closest",
                               margin=dict(t=30,r=70),
                               xaxis=dict(showline=True,
                                          showgrid=False,
                                          showticklabels=True,
                                          linecolor='black',
                                          linewidth=1,
                                          ticks='outside',
                                          tickcolor='black',
                                          tickfont=dict(family='Arial',
                                                        size=12,
                                                        color='black')),
                               yaxis=dict(title="Gross Sales ($)",
                                          visible=True,
                                          color="black",
                                          showline=True,
                                          showgrid=True))
                               
           }
    
    return fig

###########################################################################################################################################################################################################################################

#callback pie chart
@app.callback(Output("pie_chart","figure"),
               Input("year_selector","value"))

def pie_chart_plot(year):
    pie,features = function1(year,1)
    fig = {'data':[go.Pie(labels=features,
                          values=pie["total_gross"],
                          textinfo="label+percent",
                          hoverinfo="label+value+percent",
                          textfont=dict(size=13),
                          texttemplate='%{label}: <br>(%{percent})',
                          textposition='auto',
                           marker=dict(
                                        line=dict(
                                            color='lavender',
                                            width=0  )
                                      )
                           )
                  ],
           'layout': go.Layout(
                               
                                plot_bgcolor= 'lavender',
                                paper_bgcolor= 'lavender',
                                
                                title=dict(text="Sales by Rating: Year "+str(year),
                                            y=0.97,
                                            x=0.5,
                                            xanchor='center',
                                            yanchor='top',
                                            font=dict(size=177)
                                            ),
                                titlefont=dict(color="black",
                                                size=15),
                                hovermode="closest",
                                legend=dict(orientation="h",
                                            xanchor="center",
                                            yanchor="bottom",
                                            x=0.5,
                                            y=-0.35
                                            )
                                
                                
           )}
    return fig

###########################################################################################################################################################################################################################################

#callback share year 
@app.callback(Output("share_year","children"),
              [Input("year_selector","value")])
def selected_year(year):
    return """ **Percentage share** of each rated category in **{}**""".format(year)

###########################################################################################################################################################################################################################################

#callback share_table
@app.callback(Output("share_table","children"),
              [Input("year_selector","value"),Input("pie_chart","figure")])

def share_table(year,fig):
    
    pie,features = function1(year,1)
    print(len(features))
    print("asfgsasasavs")
    share = []
    
    value = fig["data"][0]["values"]
    
    s = sum(value)
    
        
    table_body_row = []
    
    for i in range(len(features)):
        
        table_body_row+=[
                            html.Tr([
                                    html.Td(features[i]),
                                    html.Td((value[i]/s)*100)
                        ],className="table_row")
        ]
    
    
    
    return html.Table([
                        html.Thead([
                                            html.Tr([
                                                        html.Th('Rating'),
                                                        html.Th("% Share in "+str(year))
                                                        
                                                        
                                                        
                                                ],className="TableHeader")
                                      ]),
                        html.Tbody(table_body_row)
                     ],className="table",style={'width': '75%'})


if __name__ == '__main__':
    app.run_server(debug=True)