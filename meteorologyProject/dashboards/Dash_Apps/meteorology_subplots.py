from os import name
import dash_core_components as dcc
from dash import html, callback_context
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from datetime import datetime, timedelta
from .dashboards_components import VaisalaDashBoard, Dummyrender, MeteoBlueDashboard

from .script import make_gif

import gif_player as gif


stations = ["Magellan", "DuPont", "C40"]

now = datetime.now() - timedelta(days=1)

now_string = now.strftime("%Y-%m-%d  %H:%M:%S")

#Create DjangoDash applicaiton
app = DjangoDash(name='Subplots', serve_locally=True)
'''
#Configure app layout
app.layout = html.Div([
                html.Div([
                    
                    #Add dropdown for option selection
                    dcc.Dropdown(
                      id = 'station',
                      options = [{'label': i, 'value': i} for i in stations],
                      value = "Magellan")],#Initial value for the dropdown
                      style={'width': '25%', 'margin':'0px auto'}),                
                    html.Button("Download CSV", id="btn_csv"),
                    dcc.Download(id="download-dataframe-csv"),
                    

                html.Div([                 
                    dcc.Graph(id = 'station_plot', 
                              animate = False, 
                              style={"backgroundColor": "#FFF0F5"}),
                    
                    dcc.Interval(id='interval-component',
                                 interval= 5 * 60000, # every 5 minutes,
                                 n_intervals=0
                             )
                              ]),
                html.Div(id='hidden-div', style={'display':'none'})
                        ])
'''        


'''
app.layout = html.Div([
                html.Div([
                    
                    #Add dropdown for option selection
                    dcc.Dropdown(
                      id = 'station',
                      options = [{'label': i, 'value': i} for i in stations],
                      value = "Magellan"),#Initial value for the dropdown
                      html.Button("Download CSV", id="btn_csv"),
                      dcc.Download(id="download-dataframe-csv")],
                      style={'width': '25%', 'margin':'0px auto', 'grid-column-start': '2', 'grid-row-start': '2'}),                                    
                    

                html.Div([                 
                    dcc.Graph(id = 'station_plot', 
                              animate = False, 
                              style={"backgroundColor": "#FFF0F5"}),
                    
                    dcc.Interval(id='interval-component',
                                 interval= 5 * 60000, # every 5 minutes,
                                 n_intervals=0
                             )
                              ], style={'grid-column-start': '1', 'grid-row-start': '1'}),
                
                html.Div([
                    dcc.Graph(id = 'weatherlco_plot',
                              figure=  df.fig,
                              animate = True, 
                              style={"backgroundColor": "#FFF0F5"})
                ], style={'grid-column-start': '2', 'grid-row-start': '1'}),

                html.Div(id='hidden-div', style={'display':'none'})
                        ], style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'grid-template-rows': '1fr 1fr'})
'''

# fig_stations_plot.fig

app.layout = html.Div([

            #Add dropdown for option selection
                    dcc.Dropdown(
                      id = 'station',
                      options = [{'label': i, 'value': i} for i in stations],
                      value = "Magellan",#Initial value for the dropdown
                      style={'width': '25%', 'margin':'0px auto'}),                
                    html.Button("Download CSV", id="btn_csv"),
                    dcc.Download(id="download-dataframe-csv"),
                    dcc.Interval(id='interval-component',
                                 interval= 5 * 60000, # every 5 minutes,
                                 n_intervals=0
                             ),
            html.Div([

                            html.Div([ 
                                dcc.Graph(id = 'seeing_plot', 
                                        animate = False,
                                        style={"backgroundColor": "#FFF0F5"}),
                            ], style={'grid-column-start': '1', 'grid-row-start': '1'}),

                            html.Div([
                                dcc.Graph(id = 'station_plot',
                                        animate = False, 
                                        style={"backgroundColor": "#FFF0F5"}),
                            ], style={'grid-column-start': '1', 'grid-row-start': '2', 'grid-row-end': 'span 2'}),

                            html.Div([
                                dcc.Graph(id = 'scattergl_plot',
                                        animate = False, 
                                        style={"backgroundColor": "#FFF0F5"}),
                            ], style={'grid-column-start': '2', 'grid-row-start': '1', 'grid-row-end': 'span 2'}),

                            html.Div([
                                    gif.GifPlayer(
                                    id= 'redanim',
                                    gif= app.get_asset_url('redanim.gif'),  #'https://clima.lco.cl/casca/redanim.gif?2905718',
                                    still= app.get_asset_url('redanimpic.png') #'https://fakeimg.pl/340x340/'
                                )
                            ], style={'grid-column-start': '2', 'grid-row-start': '3', 'margin-left': 'auto', 'margin-right': 'auto'}),
                            
                            html.Div([
                                gif.GifPlayer( 
                                    id='satanim',
                                    gif= app.get_asset_url('satanim.gif'),
                                    still= app.get_asset_url('20240201220.png')
                            )
                            ], style={'grid-column-start': '3', 'grid-row-start': '1', 'grid-row-end': '3'}),

                            

            ], style={'display': 'grid', 'grid-template-columns': '800px 340px 1fr', 'grid-template-rows': '180px 160px 1fr'}),

             html.Div(id='hidden-div', style={'display':'none'}) #This div is a dummy for using live update

])

#'https://clima.lco.cl/casca/satanim.gif?5836492'

'''
@app.callback(
        Output('satanim', 'gif'),
        Input('update_gif', 'n_clicks'))

def get_new_gif(n_clicks):  
    print(n_clicks)

    if n_clicks == 2:

        return 'https://clima.lco.cl/casca/redanim.gif?2905718'      
    return 'https://clima.lco.cl/casca/satanim.gif?5836492'
'''

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

    df.generate_stations_plot()

    return df.fig

#Define app input and output callbacks
@app.callback(
               Output('scattergl_plot', 'figure'), #id of html component
              [Input('station', 'value')]) #id of html component
              
def display_value(station):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """
    
    print("---------------Data de", station)
    df = Dummyrender(station)

    df.generate_scattergl_plot()

    return df.fig_scattergl

#Define app input and output callbacks
@app.callback(
               Output('seeing_plot', 'figure'), #id of html component
              [Input('station', 'value')]) #id of html component
              
def display_value(station):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """
    
    print("---------------Data de", station)
    df = Dummyrender(station)

    df.generate_seeing_plot()

    return df.fig_seeing
    
    
    
    #df = VaisalaDashBoard(station)

    #df.generate_dash()    


    #return df.fig
    


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"), 
    Input('station', 'value'),
    prevent_initial_call=True)

def func(*args,**kwargs):
    #
    #This function is responsible to download the csv but ONLY when the button
    #is clicked, without this function the code downloads the csv when changing
    #the dropdown or when the button is clicked because of how dash app callback 
    #inputs works.
    #
    
    
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

@app.callback(Output("hidden-div", "value"),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
   
    print(n)
    print("hola")
    #make_gif()
    
    return "lco"


