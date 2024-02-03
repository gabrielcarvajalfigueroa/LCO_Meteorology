from os import name
import dash_core_components as dcc
from dash import html, callback_context
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from datetime import datetime, timedelta
from .dashboards_components import VaisalaDashBoard, Dummyrender, MeteoBlueDashboard
from random import randint


import gif_player as gif


stations = ["Magellan", "DuPont", "C40"]

now = datetime.now() - timedelta(days=1)

now_string = now.strftime("%Y-%m-%d  %H:%M:%S")

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
app = DjangoDash(name='Subplots')

app.layout = html.Div([

            #Add dropdown for option selection
                    dcc.Dropdown(
                      id = 'station',
                      options = [{'label': i, 'value': i} for i in stations],
                      value = "Magellan",#Initial value for the dropdown
                      style={'width': '25%', 'margin':'0px auto'}),                
                    html.Button("Download CSV", id="btn_csv"),
                    html.Link(rel = "stylesheet",
                            type = "text/css",
                            href = "http://127.0.0.1:9900/stations_imgs.css"),
                    dcc.Download(id="download-dataframe-csv"),                         
                    dcc.Interval(id='interval-component',
                                 interval= 2 * 60000, # every 5 minutes,
                                 n_intervals=0
                             ),
                    dcc.Interval(id='interval-component-update',
                        interval= 5 * 60000, # every 5 minutes,
                        n_intervals=0
                    ),
            html.Div([

                            html.Div([ 
                                dcc.Graph(id = 'seeing_plot', 
                                        animate = False,
                                        config=toolbar_config,
                                        style={"backgroundColor": "#FFF0F5"}),
                            ], style={'grid-column-start': '1', 'grid-row-start': '1'}),

                            html.Div([
                                dcc.Graph(id = 'station_plot',
                                        animate = False, 
                                        config=toolbar_config,
                                        style={"backgroundColor": "#FFF0F5"}),
                            ], style={'grid-column-start': '1', 'grid-row-start': '2', 'grid-row-end': 'span 2'}),

                            html.Div([
                                dcc.Graph(id = 'scattergl_plot',
                                        animate = False, 
                                        config=toolbar_config,
                                        style={"backgroundColor": "#FFF0F5"}),
                            ], style={'grid-column-start': '2', 'grid-row-start': '1', 'grid-row-end': 'span 2'}),

                            html.Div([
                                    gif.GifPlayer(
                                    id= 'redanim',                                    
                                    gif=  "https://weather.lco.cl/casca/redanim.gif?3588110",#"http://127.0.0.1:8000/static//dpd/assets/dashboards/Dash_Apps/meteorology_subplots/satanim.gif"app.get_asset_url('redanim.gif'),  
                                    still= "https://weather.lco.cl/casca/latestred.png",    
                                    height = 340,                                
                                    width = 340
                                )
                            ], style={'grid-column-start': '2', 'grid-row-start': '3', 'margin-left': 'auto', 'margin-right': 'auto'}),
                            
                            html.Div([
                                gif.GifPlayer( 
                                    id='satanim',
                                    gif= "http://127.0.0.1:9900/satanim.gif?69",#app.get_asset_url('satanim.gif'),
                                    still= "http://127.0.0.1:9900/still.png?69",#app.get_asset_url('20240201220.png')
                                    height=10,
                                    width=10
                            )
                            ], style={'grid-column-start': '3', 'grid-row-start': '1', 'grid-row-end': 'span 3'}),

                            html.Div(id="gifdiv"),

                            

            ], style={'display': 'grid', 'grid-template-columns': '800px 340px 1fr', 'grid-template-rows': '180px 160px 1fr'}),

             html.Div(id='hidden-div', style={'display':'none'}) #This div is a dummy for using live update

])



# Callback for updating stations plot
@app.callback(
               [Output('station_plot', 'figure'),
                Output('scattergl_plot', 'figure'),
                Output('seeing_plot', 'figure')], #id of html component
              [Input('station', 'value'), Input('interval-component-update', 'n_intervals')]) #id of html component
              
def update_value(*args,**kwargs):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """

    print("---- About to Update ----", args[0])

    df = VaisalaDashBoard(args[0])
    
    df.generate_stations_plot()

    df.generate_scattergl_plot()

    df.generate_seeing_plot()

    return df.fig, df.fig_scattergl, df.fig_seeing




# Callback for downloading csv 
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
        data = VaisalaDashBoard(args[1])

        return dcc.send_data_frame(data.df.to_csv, f"{args[1]}-{now_string}.csv")


# Callback for updating gifs
@app.callback([Output("satanim", "gif"),
               Output("satanim", "still")],
              [Input('interval-component', 'n_intervals')],
              prevent_initial_call=True)
def update_metrics(n):
    
    print("--------------------------")
    print("ABOUT TO UPDATE GIF")
    print("--------------------------")

    print(n)    

    gif = "http://127.0.0.1:9900/satanim.gif?" + str(randint(100,999))
    still = "http://127.0.0.1:9900/still.png?" + str(randint(100,999))
        

    return gif, still
    
    #if n%2==0:
    #return "https://clima.lco.cl/casca/satanim.gif?4621460", app.get_asset_url('20240201220.png')


