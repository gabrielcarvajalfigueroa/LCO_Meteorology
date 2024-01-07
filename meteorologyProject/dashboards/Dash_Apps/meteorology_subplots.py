from os import name
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from datetime import datetime, timedelta
from .dashboards_components import VaisalaDashBoard


stations = ["Magellan", "DuPont", "C40"]

now = datetime.now() - timedelta(days=1)

now_string = now.strftime("%Y-%m-%d  %H:%M:%S")

#Create DjangoDash applicaiton
app = DjangoDash(name='Subplots')

#Configure app layout
app.layout = html.Div([
                html.Div([
                    
                    #Add dropdown for option selection
                    dcc.Dropdown(
                      id = 'station',
                      options = [{'label': i, 'value': i} for i in stations],
                      value = "Magellan")],#Initial value for the dropdown
                    style={'width': '25%', 'margin':'0px auto'}),
                    dcc.DatePickerSingle(
                        month_format='Y-M-D',
                        placeholder='Y-M-D',
                        date=now_string
                    ),
                    html.Button('Set Date to Now'),

                html.Div([                 
                    dcc.Graph(id = 'station_plot', 
                              animate = True, 
                              style={"backgroundColor": "#FFF0F5"})
                              ])
                        ])

#Define app input and output callbacks
#'''
@app.callback(
               Output('station_plot', 'figure'), #id of html component
              [Input('station', 'value')]) #id of html component
              
def display_value(station):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """

    df = VaisalaDashBoard(station)

    df.generate_dash()    


    return df.fig

# Callback for live updating
#'''
'''
@app.callback(Output('station_plot', 'extendData'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    now = datetime.now() - timedelta(days=1)

    now_string = now.strftime("%Y-%m-%d  %H:%M:%S")
    
    fig = dash_plotly_plot("Magellan", now_string)
    
    return fig
'''    