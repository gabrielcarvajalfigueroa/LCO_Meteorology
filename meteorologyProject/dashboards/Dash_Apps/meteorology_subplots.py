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

def dash_plotly_plot(station, now_string):
    """
    This function creates dash app 
    Output: Figure object
    """

    m = dataclient.VaisalaData.parameters(station = station,
                               start_ts = '2024-01-04 14:00:00',                                                                  
                               limit = '1440')

    df = dataclient.DataService.get(m)

    df.sort_index(inplace=True)

    df['time'] = df.index

    print("El tipo del DF ES",type(dataclient.DataService.get(m)))

    print(df.isnull().values.any())
    df.dropna(subset=['temperature'], inplace=True)

    fig = make_subplots(rows=3, cols=2,
                    shared_xaxes=True,
                    vertical_spacing=0.02,                    
                    specs=[[{"type": "xy"}, {"type": "polar", "rowspan": 3}],
                          [{"type": "xy"}, {"type": "polar"}],
                          [{"type": "xy"}, {"type": "polar"}]],)
    
    

    fig.add_trace(go.Scatter(x=df['time'], y=df['temperature'], name="Temperature"),
              row=3, col=1)

    fig.add_trace(go.Scatter(x=df['time'], y=df['wind_speed_avg'], name="Wind"),
              row=2, col=1)
    
    fig.add_trace(go.Scatter(x=df['time'], y=df['wind_speed_min'], name="WindMin"),
              row=2, col=1)
    
    fig.add_trace(go.Scatter(x=df['time'], y=df['wind_speed_max'], name="WindMax"),
              row=2, col=1)

    fig.add_trace(go.Scatter(x=df['time'], y=df['air_pressure'], name="Pressure"),
              row=1, col=1)
    
    
    fig.add_trace(go.Scatterpolargl(
      r = df.wind_speed_avg,
      theta = df.wind_dir_avg,
      name = "Wind AVG",
      mode = "markers",
      marker=dict(size=15, color="mediumseagreen")      
    ),row=1,
      col=2)
    
    fig.add_trace(go.Scatterpolargl(
      r = df.wind_speed_min,
      theta = df.wind_dir_min,
      name = "Wind MIN",
      mode = "markers",
      marker=dict(size=20, color="gold", opacity=0.7)      
    ),row=1,
      col=2)
    
    fig.add_trace(go.Scatterpolargl(
      r = df.wind_speed_max,
      theta = df.wind_dir_max,
      name = "Wind MAX",
      mode="markers",
      marker=dict(size=12, color="red", opacity=0.7)      
    ),row=1,
      col=2)


    fig['layout']['yaxis']['title']='Pressure'
    fig['layout']['yaxis2']['title']='Wind'
    fig['layout']['yaxis3']['title']='Temperature'


    #fig.update_traces(mode="markers", marker=dict(line_color='white', opacity=0.7))

    fig.update_layout(title_text=now_string,
                      font_size = 15, height=700,
    showlegend = True,
    polar = dict(
      bgcolor = "rgb(223, 223, 223)",
      angularaxis = dict(
        linewidth = 3,
        showline=True,
        linecolor='black'
      ),
      radialaxis = dict(
        side = "counterclockwise",
        showline = True,
        linewidth = 2,
        gridcolor = "white",
        gridwidth = 2,
      )
    ),
    paper_bgcolor = "rgb(223, 223, 223)")


    
    return fig


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
    #Get city plot with input value
    now = datetime.now() - timedelta(days=1)

    now_string = now.strftime("%Y-%m-%d  %H:%M:%S")
    
    fig = dash_plotly_plot(station, now_string)
    
    return fig

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