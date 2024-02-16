import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from datetime import datetime, timedelta
from .dashboards_components import VaisalaDashBoard

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
app = DjangoDash(name='History', serve_locally=True)

app.layout = html.Div([
                            #Add dropdown for option selection
                            dcc.Dropdown(
                            id = 'station',
                            options = [{'label': i, 'value': i} for i in stations],
                            clearable = False,
                            value = "Magellan", #Initial value for the dropdown
                            style={'width': '25%', 'margin':'0px auto'}),                
                            html.Button("Download CSV", id="btn_csv"),
                            dcc.Download(id="download-dataframe-csv"),
                    
            html.Div([
                            # Displays Seeing Plot
                            html.Div([ 
                                dcc.Graph(id = 'seeing_plot', 
                                        animate = False,
                                        config=toolbar_config,
                                        style={"backgroundColor": "#FFF0F5"}),
                            ], style={'grid-column-start': '1', 'grid-row-start': '1'}),

                            # Displays Station plot
                            html.Div([
                                dcc.Graph(id = 'station_plot',
                                        animate = False, 
                                        config=toolbar_config,
                                        style={"backgroundColor": "#FFF0F5"}),
                            ], style={'grid-column-start': '1', 'grid-row-start': '2', 'grid-row-end': 'span 2'}),

                            # Displays Polar Chart for Wind speed and direction
                            html.Div([
                                dcc.Graph(id = 'scattergl_plot',
                                        animate = False, 
                                        config=toolbar_config,
                                        style={"backgroundColor": "#FFF0F5"}),
                            ], style={'grid-column-start': '2', 'grid-row-start': '1', 'grid-row-end': 'span 2'}),

                            # Displays Date for the calendar
                            html.Div([
                                dcc.DatePickerSingle(
                                        id='history-date-picker',
                                        placeholder="Click here"
                                    ),
                            ], style={'grid-column-start': '3', 'grid-row-start': '1'}) 
                        
            ], style={'display': 'grid', 'grid-template-columns': '800px 340px 1fr', 'grid-template-rows': '180px 160px 1fr'}),        
])



# Callback for updating stations plot
@app.callback(
               [Output('station_plot', 'figure'),
                Output('scattergl_plot', 'figure'),
                Output('seeing_plot', 'figure'),
                Output('history-date-picker', 'min_date_allowed'),
                Output('history-date-picker', 'max_date_allowed')], #id of html component
              [Input('station', 'value'), Input('history-date-picker', 'date')],
              prevent_initial_call=False) #id of html component
              
def update_value(*args,**kwargs):
    """
    This function returns all the plotly figure objects neccesary to display the
    whole dashboard in this case 3 figures
    Input-1: Station -> Magellan, Dupont or C40
    Input-2: Date for selecting when to fetch data
    Output: Figure object
    """
    # args[0]: station value eg. Magellan
    # args[1]: date selected eg. 2024-02-01 -> str        

    # It's neccesary to update min and max dates otherwise it gets stucks with the
    # initial dates.
    min_date_allowed = datetime.now() - timedelta(days=14)
    max_date_allowed = datetime.now() - timedelta(days=1)

    # Uses ctx to check if it is the first time the callback is displayed
    # This is useful to display the data from the day before when the page is called.
    ctx = kwargs['callback_context']
    
    # Conditionals explanation
    # len(ctx.triggered) --> To check if it was the initial call when rendering the page or not
    # args[1] -------------> This is in case the user changes a station without selecting a date

    if len(ctx.triggered) != 0 and args[1] != None:

        start_ts = datetime.strptime(args[1] + " 00:00:00", '%Y-%m-%d %H:%M:%S')

        end_ts = start_ts + timedelta(days=1)

        start_ts = start_ts.strftime("%Y-%m-%d %H:%M:%S")
        end_ts = end_ts.strftime("%Y-%m-%d %H:%M:%S")

        df = VaisalaDashBoard(args[0], start_ts, end_ts)
        
        df.generate_stations_plot()

        df.generate_scattergl_plot()

        df.generate_seeing_plot()
        
        return df.fig, df.fig_scattergl, df.fig_seeing, min_date_allowed, max_date_allowed

    else:

        # This is the logic to display the first data whichs is the one
        # from the day before.

        now = datetime.now() - timedelta(days=1)

        start_ts = now.replace(hour=0, minute=0, second=0, microsecond=0)

        end_ts = start_ts + timedelta(days=1)

        start_ts = start_ts.strftime("%Y-%m-%d %H:%M:%S")
        end_ts = end_ts.strftime("%Y-%m-%d %H:%M:%S")        

        df = VaisalaDashBoard(args[0], start_ts, end_ts)
        
        df.generate_stations_plot()

        df.generate_scattergl_plot()

        df.generate_seeing_plot()
        
        return df.fig, df.fig_scattergl, df.fig_seeing, min_date_allowed, max_date_allowed


# Callback for downloading csv 
@app.callback(
    Output("download-dataframe-csv", "data"),
    [Input("btn_csv", "n_clicks"), Input('station', 'value'), Input('history-date-picker', 'date')],
    prevent_initial_call=True)

def download_csv(*args,**kwargs):
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
        # args[2]: selected date

        if args[2] != None:
            start_ts = datetime.strptime(args[2] + " 00:00:00", '%Y-%m-%d %H:%M:%S')

            end_ts = start_ts + timedelta(days=1)

            start_ts = start_ts.strftime("%Y-%m-%d %H:%M:%S")
            end_ts = end_ts.strftime("%Y-%m-%d %H:%M:%S")

            data = VaisalaDashBoard(args[1], start_ts, end_ts)        

            return dcc.send_data_frame(data.df.to_csv, f"{args[1]}-{start_ts[:10]}.csv")
        
        else:
            # If there was no selected date it sends the data from yesterday

            now = datetime.now() - timedelta(days=1)

            start_ts = now.replace(hour=0, minute=0, second=0, microsecond=0)

            end_ts = start_ts + timedelta(days=1)

            start_ts = start_ts.strftime("%Y-%m-%d %H:%M:%S")
            end_ts = end_ts.strftime("%Y-%m-%d %H:%M:%S") 

            data = VaisalaDashBoard(args[1], start_ts, end_ts)        

            return dcc.send_data_frame(data.df.to_csv, f"{args[1]}-{start_ts[:10]}.csv")



