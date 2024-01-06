from os import name
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from plotly.subplots import make_subplots
from lcodataclient import dataclient
from datetime import datetime, timedelta


def meteoblue_plotly_plot():
    m = dataclient.MeteoblueData.parameters()

    df = dataclient.DataService.get(m)

    # The x-axis needs to be sorted otherwise the plot will not work properly
    df.sort_index(inplace=True)

    df['time'] = df.index

    print(df)

    df.dropna(subset=['temperature'], inplace=True)

    fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02,                    
                    specs=[[{"type": "xy"}],
                          [{"type": "xy"}],
                          [{"type": "xy"}]],)
    
    

    fig.add_trace(go.Scatter(x=df['time'], y=df['temperature'], name="Temperature"),
              row=1, col=1)

    fig.add_trace(go.Scatter(x=df['time'], y=df['winddirection'], name="Precipitation"),
              row=2, col=1)
    
    fig.add_trace(go.Scatter(x=df['time'], y=df['relativehumidity'], name="Wind"),
              row=3, col=1)


    fig['layout']['yaxis']['title']='Temperature'
    fig['layout']['yaxis2']['title']='Precipitation'
    fig['layout']['yaxis3']['title']='Wind'


    fig.update_layout(title_text="Weather LCO Meteoblue",
                      font_size = 15, height=700,
    showlegend = True,
    paper_bgcolor = "rgb(223, 223, 223)")
    
    return fig


#Create DjangoDash applicaiton
app = DjangoDash(name='Meteoblue')

#Configure app layout
app.layout = html.Div([                             
                    dcc.Graph(id = 'weatherlco_plot', 
                            animate = True, 
                            style={"backgroundColor": "#FFF0F5"})                                                        
                    ])