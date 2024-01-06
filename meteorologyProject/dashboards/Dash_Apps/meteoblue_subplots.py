from os import name
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from plotly.subplots import make_subplots
from lcodataclient import dataclient
from datetime import datetime


def meteoblue_plotly_plot():
    m = dataclient.MeteoblueData.parameters()

    df = dataclient.DataService.get(m)

    # The x-axis needs to be sorted otherwise the plot will not work properly
    df.sort_index(inplace=True)

    df['time'] = df.index

    df.dropna(subset=['temp'], inplace=True)

    fig = make_subplots(rows=3, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02,                    
                    specs=[[{"type": "xy"}],
                          [{"type": "xy"}],
                          [{"type": "xy"}]],)
    
    

    fig.add_trace(go.Scatter(x=df['time'], y=df['temp'], name="Temperature"),
              row=1, col=1)

    fig.add_trace(go.Scatter(x=df['time'], y=df['relativehumidity'], name="Precipitation"),
              row=2, col=1)
    
    # WARNING: This code is for adding the precipitation but is not linked to the data 
    fig.add_hrect(y0=26, y1=30, fillcolor="brown", opacity=0.4, row=2, col=1 )
    
    fig.add_trace(go.Scatter(x=df['time'], y=df['windspeed'], name="Wind"),
              row=3, col=1)
    

    #TODO: Find the max_wind_spedd as an integer
    # And use: [max_wind_speed] * len(df) for setting the y value.
    max_temp = df.loc[df['temp'].idxmax()]
    min_temp = df.loc[df['temp'].idxmin()]    

    #max_wind_speed = df.loc[df['windspeed'].idxmax()]
    #Converts the max_wind_speed to a list for obtaining the top limit for the arrows
    #max_wind_speed = max_wind_speed['windspeed'] * len(df)

    #This trace is por adding the wind direction
    fig.add_trace(go.Scatter(
                x=df['time'],
                y=[7] * len(df),
                mode='markers',
                line=dict(color='blue'),
                marker=dict(
                    color='blue',
                    size=20,
                    symbol='arrow',
                    angle=df['winddirection']
    )), row=3, col=1)


    fig['layout']['yaxis']['title']='Temperature'
    fig['layout']['yaxis2']['title']='Precipitation'
    fig['layout']['yaxis3']['title']='Wind'

    # Adds a dash line for the actual time
    now = datetime.now()

    now_string = now.strftime("%Y-%m-%d %H:%M:%S")    

    fig.add_vline(x=now_string, line_width=3, line_dash="dash", line_color="black")

    # Following code explanation
    # check: https://stackoverflow.com/questions/63731256/how-to-show-ranges-of-repeated-values-in-a-colum-in-python-pandas
    (df.update((df.astype(str)).groupby((df.isdaylight!=df.isdaylight.shift())\
    .cumsum())["time"].transform(lambda x: x.iloc[0]+'+'+x.iloc[-1])))
    df = df[['isdaylight', 'time']]
    df=df.drop_duplicates()


    for index, row in df.iterrows():
        if row['isdaylight']:            
            x_axis = row['time'].split("+")

            #This code is for adding the sun time
            fig.add_vrect(x0=x_axis[0], x1=x_axis[1], row="all", col=1,
                    annotation_text="", annotation_position="top left",
                    fillcolor="yellow", opacity=0.25, line_width=0.2)
            #Adds the maximum value for temperature
            fig.add_annotation(x=max_temp['time'],
                               y=max_temp['temp'],
                               text=max_temp['temp'],
                               row=1,
                               col=1)
            #Adds the minimum value for temperature
            fig.add_annotation(x=min_temp['time'],
                               y=min_temp['temp'],
                               text=min_temp['temp'],
                               row=1,
                               col=1)
                    

    fig.update_layout(title_text="LCO <br><sup>20.01°S / 70.69°W (2365m asl)</sup>",
                      font_size = 15,
                      height=700,
                      showlegend = True,
                      paper_bgcolor = "rgb(223, 223, 223)",
                      autotypenumbers='convert types')
    
    return fig


#Create DjangoDash applicaiton
app = DjangoDash(name='Meteoblue')

# Maybe it will be neccesary to add lambda for reloading the page correctly
# check: https://stackoverflow.com/questions/54192532/how-to-use-dash-callback-without-an-input
#Configure app layout
app.layout = html.Div([                             
                    dcc.Graph(id = 'weatherlco_plot',
                              figure=  meteoblue_plotly_plot(),
                            animate = True, 
                            style={"backgroundColor": "#FFF0F5"})                                                        
                    ])

#Callback to display de graphs

@app.callback(Output('weatherlco_plot', 'figure'))

def display_value():

    fig = meteoblue_plotly_plot()

    return fig