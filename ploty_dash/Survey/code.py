import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go

#Scatter plot

np.random.seed(42)

x = np.random.randint(1,101,100)
y = np.random.randint(1,101,100)

data = [go.Scatter(x=x,y=y,
                   mode='markers',
                   marker=dict(
                       size=8,color='rgb(60,66,252)',symbol='square',line={'width':2}
                   ))]

layout = go.Layout(title='Scatter plot',
                   xaxis=dict(title='X axis'),yaxis=dict(title='Y axis'),
                   hovermode = 'closest')

fig = go.Figure(data,layout)
pyo.plot(fig,filename='scatter.html')

#%%
import numpy as np
import plotly.offline as pyo
import plotly.graph_objs as go

#Line chart

x = np.linspace(0,1,100)
y = np.random.randn(100)

trace = go.Scatter(x=x,y=y+5,
                   mode='markers',
                   name='markers')

trace1 = go.Scatter(x=x,y=y,
                   mode='lines',
                   name='Line chart')

trace2 = go.Scatter(x=x,y=y-5,
                   mode='lines+markers',
                   name='Line+Markers')

data = [trace,trace1,trace2]

layout = go.Layout(title="Line chart")

fig = go.Figure(data,layout)
pyo.plot(fig,filename='linechart.html')




# %%
import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

#linechart for dataset


data = pd.read_csv('nst-est2017-alldata.csv')
data.info()
data = data[data['DIVISION']=='1']
data.set_index("NAME",inplace=True)
data = data[[col for col in data.columns if col.startswith("POP")]]
data

df = [go.Scatter(x=data.columns,y=data.loc[name],
                 mode='lines',name=name) for name in data.index]

pyo.plot(df,filename='linechart_fordataset.html')

# %%

import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

#linechart_Exercise

data = pd.read_csv("2010YumaAZ.csv")
data.info()
days=list(data["DAY"].unique())
data.head()

df = [go.Scatter(x=data["LST_TIME"],y=data[data["DAY"]==d]["T_HR_AVG"],
                 mode='lines',name=d) for d in days]
pyo.plot(df,filename='linechart_exercises.html')
# %%

import numpy as np
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

#Bar Plot

data = pd.read_csv("2018WinterOlympics.csv")
data.info()
data.head(10)

trace1 = go.Bar(x=data["NOC"],y=data['Gold'],name='Gold',marker = {'color':'#FFD700'} )

trace2 = go.Bar(x=data["NOC"],y=data['Silver'],name='Silver',marker = {'color':'#9EA0A1'} )

trace3 = go.Bar(x=data["NOC"],y=data['Bronze'],name='Bronze',marker = {'color':'#CD7F32'} )


df = [trace1,trace2,trace3]
layout = go.Layout(title="2018 WINTER OLYMPICS",barmode='stack')

fig = go.Figure(data=df,layout=layout)

pyo.plot(fig,filename="Barplot.html")


# %%

import numpy as np

import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

#bar plot exercise

data = pd.read_csv("mocksurvey.csv")
data.info()
data.head()

col = list(data.columns)[1::]
col=list(col)
df = [go.Bar(x=data["Unnamed: 0"],y=data[m],name=m) for m in col]

layout = go.Layout(title="Mock Survey",barmode="stack")

fig = go.Figure(data=df,layout=layout)

pyo.plot(fig,filename="barplot_exercise.html")


# %%
import numpy as np

import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

#bubble plot 
data = pd.read_csv("mpg.csv")
data.info()
data.head()


df = [go.Scatter(x=data["horsepower"],y=data["mpg"],
                 text=data["name"],
                 mode="markers",
                 marker=dict(size=2*data["cylinders"],
                             color = data["cylinders"],
                             showscale = True))]

layout = go.Layout(title="Bubble plot",hovermode='closest')

fig = go.Figure(layout=layout,data=df)

pyo.plot(fig,filename="bubbleplot.html")
# %%
import numpy as np

import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

#bubble plot exercise
data = pd.read_csv("mpg.csv")
data.info()
data.head()


df = [go.Scatter(x=data["displacement"],y=data["acceleration"],
                 text=data["name"],
                 mode="markers",
                 marker=dict(size=data["weight"]/100,
                             color = data["weight"],
                             showscale = True))]

layout = go.Layout(title="Bubble plot",hovermode='closest')

fig = go.Figure(layout=layout,data=df)

pyo.plot(fig,filename="bubbleplot_exercise.html")

# %%
