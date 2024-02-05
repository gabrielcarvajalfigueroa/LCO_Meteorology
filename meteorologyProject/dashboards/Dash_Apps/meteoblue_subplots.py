from os import name
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import pandas as pd
from .dashboards_components import MeteoBlueDashboard


import os


df = MeteoBlueDashboard()

df.generate_dash()

toolbar_config = {"displayModeBar": True,
                 "displaylogo": False,
                 'modeBarButtonsToRemove': [
                     'zoomin',
                     'zoomout',
                     'zoom',
                     'pan2d',
                     'autoScale2d',
                     'resetScale2d',
                     'lasso',
                     'select2d']}

#Create DjangoDash applicaiton
app = DjangoDash(name='Meteoblue')

# Maybe it will be neccesary to add lambda for reloading the page correctly
# check: https://stackoverflow.com/questions/54192532/how-to-use-dash-callback-without-an-input
#Configure app layout

app.layout = html.Div([                             
                    dcc.Graph(id = 'weatherlco_plot',
                              figure=  df.fig,
                              animate = True, 
                              config = toolbar_config,
                              style={"backgroundColor": "#FFF0F5"})                                                        
                    ])

