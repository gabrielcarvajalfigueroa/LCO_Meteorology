from dash import html, dcc
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from datetime import datetime, timedelta
from .dashboards_components import VaisalaDashBoard
import plotly.graph_objs as go

import gif_player as gif

# Stations to Display
stations = ["Magellan", "DuPont", "C40"]

# Toolbar that comes with the Plotly Graph
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

#Create DjangoDash application
app = DjangoDash(name='Subplots')

app.layout = html.Div([
                    dcc.ConfirmDialog(
                        id='confirm-danger',
                        message='ERROR: Couldnt fetch data for displaying',
                    ),

                    #Add dropdown for option selection
                    dcc.Dropdown(
                      id = 'station',
                      options = [{'label': i, 'value': i} for i in stations],
                      clearable = False,
                      value = "Magellan",#Initial value for the dropdown
                      style={'width': '25%', 'margin':'0px auto'}),  

                    # Button for Downloading CSV
                    html.Button("Download CSV", id="btn_csv"),                    

                    # This components sends the requested data
                    dcc.Download(id="download-dataframe-csv"),                    

                    # Live update component for updating the graphs each minute
                    dcc.Interval(id='interval-component-update',
                        interval= 1 * 60000, # every 1 minute,
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
                            gif=  "https://clima.lco.cl/casca/redanim.gif?3588110",
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

            ], style={'display': 'grid', 'grid-template-columns': '800px 340px 1fr', 'grid-template-rows': '180px 160px 1fr'}),
])


# Callback for updating stations plot
@app.callback(
               [Output('station_plot', 'figure'),
                Output('scattergl_plot', 'figure'),
                Output('seeing_plot', 'figure'),
                Output('confirm-danger', 'displayed')], #id of html component
              [Input('station', 'value'), Input('interval-component-update', 'n_intervals')]) #id of html component
              
def update_value(*args,**kwargs):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """
    try:
        df = VaisalaDashBoard(args[0])
        
        df.generate_stations_plot()

        df.generate_scattergl_plot()

        df.generate_seeing_plot()

        display_error = False

        return df.fig, df.fig_scattergl, df.fig_seeing, display_error
    
    except:
        display_error = True

        return go.Figure(), go.Figure(), go.Figure(), display_error
    


# Callback for downloading csv 
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"), 
    Input('station', 'value'),
    prevent_initial_call=True)

def func(*args,**kwargs):
    """
    This function is responsible to download the csv but ONLY when the button
    is clicked, without this function the code downloads the csv when changing
    the dropdown or when the button is clicked because of how dash app callback 
    inputs works.
    """    
    
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

        now = datetime.now() - timedelta(days=1)

        now_string = now.strftime("%Y-%m-%d  %H:%M:%S")

        return dcc.send_data_frame(data.df.to_csv, f"{args[1]}-{now_string[:10]}.csv")
