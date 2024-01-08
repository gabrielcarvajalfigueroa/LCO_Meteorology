from os import name
import dash_core_components as dcc
from dash import html, callback_context
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from datetime import datetime, timedelta
from .dashboards_components import VaisalaDashBoard, Dummyrender


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
                    dcc.DatePickerRange(end_date=now,
                                        display_format='MMM Do, YY',
                                        start_date_placeholder_text='MMM Do, YY'
                                    ),
                    html.Button('Set Date to Now'),
                    html.Button("Download CSV", id="btn_csv"),
                    dcc.Download(id="download-dataframe-csv"),

                html.Div([                 
                    dcc.Graph(id = 'station_plot', 
                              animate = False, 
                              style={"backgroundColor": "#FFF0F5"})
                              ])
                        ])

#Define app input and output callbacks
@app.callback(
               Output('station_plot', 'figure'), #id of html component
              [Input('station', 'value')]) #id of html component
              
def display_value(station):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """
    
    print("---------------Data de", station)
    df = Dummyrender(station)

    df.generate_dash()

    return df.fig
    
    
    '''
    df = VaisalaDashBoard(station)

    df.generate_dash()    


    return df.fig
    '''


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"), 
    Input('station', 'value'),
    prevent_initial_call=True)

def func(*args,**kwargs):
    '''
    This function is responsible to download the csv but ONLY when the button
    is clicked, without this function the code downloads the csv when changing
    the dropdown or when the button is clicked because of how dash app callback 
    inputs works.
    '''
    
    # In Django_plotly_dash is necessary to use kwargs otherwise it wont work
    # For more info check:
    # https://stackoverflow.com/questions/76686162/handling-different-actions-based-on-click-event-and-search-in-django-plotly-dash
    ctx = kwargs['callback_context']
    
    # The context is received as a list with a dictionary inside thats why
    # you have to call [0] and the .get('prop_id')
    if ctx.triggered[0].get('prop_id') == 'btn_csv.n_clicks':
        # The input values are recived as args
        # args[0]: btn_csv.n_clicks
        # args[1]: station.value
        data = Dummyrender(args[1])

        return dcc.send_data_frame(data.df.to_csv, f"{args[1]}-{now_string}.csv")


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