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
                      clearable = False,
                      value = "Magellan",#Initial value for the dropdown
                      style={'width': '25%', 'margin':'0px auto'}),                
                    html.Button("Download CSV", id="btn_csv"),                    
                    dcc.Download(id="download-dataframe-csv"),                         
                    dcc.Interval(id='interval-component',
                                 interval= 5 * 60000, # every 5 minutes,
                                 n_intervals=0
                             ),
                    dcc.Interval(id='interval-component-update',
                        interval= 1 * 60000, # every 5 minutes,
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
                                    gif=  "https://clima.lco.cl/casca/redanim.gif?3588110",#"http://127.0.0.1:8000/static//dpd/assets/dashboards/Dash_Apps/meteorology_subplots/satanim.gif"app.get_asset_url('redanim.gif'),  
                                    still= "https://clima.lco.cl/casca/latestred.png",    
                                    height = 340,                                
                                    width = 340
                                )
                            ], style={'grid-column-start': '2', 'grid-row-start': '3', 'margin-left': 'auto', 'margin-right': 'auto'}),

                            html.Div([
                                html.Iframe(
                                    src="https://www.meteoblue.com/en/weather/maps/widget/LCO_-29.014N-70.693E2365_UTC?windAnimation=0&gust=0&satellite=0&satellite=1&cloudsAndPrecipitation=0&temperature=0&sunshine=0&extremeForecastIndex=0&geoloc=fixed&tempunit=C&windunit=km%252Fh&lengthunit=metric&zoom=5&autowidth=auto",
                                    width=680,
                                    height=680
                                )
                            ], style={'grid-column-start': '3', 'grid-row-start': '1', 'grid-row-end': 'span 3'}),
                            
                            
                            #html.Div([
                            #    gif.GifPlayer( 
                            #        id='satanim',
                            #        gif= "https://weather.lco.cl/casca/satanim.gif",#app.get_asset_url('satanim.gif'),
                            #        still= "https://lh3.googleusercontent.com/fife/AGXqzDkJ2PMyAXYx94VyQR8TrpzukMF7-l7oU6Lbzrhr5kZwX7g6XzzUmKp9Qj-eoAx9dqnyN_zvNdlALT8QF9ILHwqjVCO0GMhp2bf3BYMzsTJ5PBSy49BqDC7DP4dMvjT1xUIuZKK-qWKDW9zuFczxeUPWtyH9ePG5L5fjZMysqBA4_0FdZLZBVfaFlr_EIYrqojWAwEX1hMRIx6EKa4jC-SSnfI3t5VeN3vuU6WoSGnoZ01QAxP3dP5iInKiNyrobimmShJeEyaS-3Db5KnIT0JyqAIMZKfZsdpNEquk9a9P5UHOS4AfyVS23SI7Vh6yoYct5F5wKCZctYHOYFoYy0P3dfSD_cnN7gIHHHL0MFILbouv9cbaYloz5K97oopk_g6ncs0Hhpz27E2AIjJrDF2IFDNmKZJWKU6_lQcI6VZ3gLk_94AXOKp5TiJEwoSYD6cX4jSSRC472lNL4rzGu5Csh3MqWgE896u6KQzbHMqwU_Nlkq3YEP-2JiYFgcWi7eSTCb3Rpi0zycfYGOn0lz4sQv1knsm-Gn3P6V7feXGabbVx3FETFDs8evEJfV6DALTPVMCHMtfoezcN0yUkZykCh2pBs4BVAZMECzCwzb0EJldJwuL7Y_P8tRhv-A3LIt-tdJ0KfIo-4FEoQfYnl9WQV_KtmCfKy7vLqOYcWfq4Cyoc_pGL0ZYCfoPBeoLjEnDyOMDrAvIkFB2lFw7Wubxgs1oU9Spjr3p9AuYVcPQ_O_tqNg3ndRAdX5dr3pdlXEjy_PeMzOXJ83bAS5XIqzpFpoBSOSPdvcbIJojtosMv0dkPLooeF27m_5-UxEDMxe7Ns7PYS2rDtHhWz4NrDMbpsxrpbIc8Yqe-apTlFGTt_pPOgb7rscw5B3ck6uWmnF25AcgynI4kbP4yteZJmEOQQKxY_gFRuf6Jz69UQTaEXBH3k_1ErBcAv2WhMi1PO8HU6Z-3kmfOHTFYVKY3JLV4T_bzYlVivtmIaqW1CqHnobVZF92r387ALJa_luKq94TszBQsmoKuGHqioe_4jbx2pA2sYzWwLL0Kt1dbGjRZ7RBZOOkMucG0scP6vtaP6YurR073oJSCi2DgYA_QvodT48z1IlAWFTizkJfHf2aNl1Cc-M0YADut4c8fzogHetqdEkI7UWN3FWKevZe-BD80MDoqIG7-Zkl30O9lav8_nUGoylFtOq1rpohCjoo8aatj4lBh2SZ3cOFIRCcNMUnpw4Z5RyDAHOCLQgekahRa8SRpZyCb0cOr9nrCsGqjV1YPFS9rWCQwlHnsk5QglKm2U2L76-oX4r-DmYiRe18XtUXcr8xU9ppQhEU80KLVsiQlQGW2IcqTnXFsBImdXJgP2-0qZmydB08bLN-3qto1EfD48L_eikZb4SdxU_p4Wl6w0Ev-gT2tlh4j8JU-Ca0rPQPWYsWcHhd9FaxZUpOP2TCuNoqERUyF6iPUsnpxQAW-fkQDKiv3F-1ALPM_VtjgbOTiCiyOd_inIpDC3s6s6yrYrVkzUY1nPG05nQCNUWlnvJO7iWwfgRn8bxi7y7Fgp0J6lVZeoS96l8c4Klvy2tWWeFEJwlcsYRJiTNQQWziWmK1agKK4EP3Vwrr3uNA=w1919-h918",#app.get_asset_url('20240201220.png')
                            #        height=680,
                            #        width=680
                            #)
                            #], style={'grid-column-start': '3', 'grid-row-start': '1', 'grid-row-end': 'span 3'}),
                            

                            html.Div(id="gifdiv"),

                            

            ], style={'display': 'grid', 'grid-template-columns': '800px 340px 1fr', 'grid-template-rows': '180px 160px 1fr'}),

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

'''
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


'''