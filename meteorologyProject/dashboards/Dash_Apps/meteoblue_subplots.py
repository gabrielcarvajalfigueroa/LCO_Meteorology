from os import name
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import pandas as pd
from .dashboards_components import MeteoBlueDashboard


import os


#df = MeteoBlueDashboard()

#df.generate_dash()

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

days = ["1 day", "3 days", "5 days"]

app.layout = html.Div([

                    dcc.Dropdown(
                      id = 'days',
                      options = [{'label': i, 'value': i} for i in days],
                      clearable = False,
                      value = "5 days",#Initial value for the dropdown
                      style={'width': '25%', 'margin':'0px auto'}),

                    dcc.Graph(id = 'meteoblue_plot',
                              animate = False, 
                              config = toolbar_config,
                              style={"backgroundColor": "#FFF0F5"})                                                        
                    ])

# Callback for updating stations plot
@app.callback(
               [Output('meteoblue_plot', 'figure')], #id of html component
              [Input('days', 'value')]) #id of html component
              
def update_value(*args,**kwargs):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """
    # args[0] = 1 days
    # args[0][:1] = 1

    df = MeteoBlueDashboard(args[0][:1])
    
    df.generate_dash()

    return [df.fig]

