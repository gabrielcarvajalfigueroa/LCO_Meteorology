import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from plotly.subplots import make_subplots
from lcodataclient import dataclient
from datetime import datetime

class MeteoBlueDashboard():
    '''Class for MeteoBlue dashboard generation'''

    def __init__(self) -> None:
        '''
        Init instance.
        :rtype: None
        '''
        m = dataclient.MeteoblueData.parameters()

        data = dataclient.DataService.get(m)

        self.df= data
        self.fig = None #This is the plotly figure to display

    def create_subplots(self) -> None:
        '''
        Creates a subplot with 3 scatter plots to display Temperature, Precipitation, Wind
        and WindDirection.
        :rtype = None
        '''
        df = self.df
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
        
        fig.add_trace(go.Scatter(x=df['time'], y=df['windspeed'], name="Wind"),
                row=3, col=1)
        
        # Shows the name of the graph in y-axis
        fig['layout']['yaxis']['title']='Temperature'
        fig['layout']['yaxis2']['title']='Precipitation'
        fig['layout']['yaxis3']['title']='Wind'

        # Adds a dash line for the actual time
        now = datetime.now()

        now_string = now.strftime("%Y-%m-%d %H:%M:%S")    

        fig.add_vline(x=now_string, line_width=3, line_dash="dash", line_color="black")

        self.fig = fig

    def fill_temperature_subplot(self) -> None:
        '''
        Fills temperature subplot using the dataframe.
        TODO: Fix the dataframe changing after using df.update()
        :rtype: None
        '''

        df_aux = self.df
        fig = self.fig

        df = df_aux

        (df.update((df.astype(str)).groupby((df.isdaylight!=df.isdaylight.shift())\
        .cumsum())["time"].transform(lambda x: x.iloc[0]+'+'+x.iloc[-1])))
        df_max_min = df[['isdaylight', 'time']]
        df_max_min=df_max_min.drop_duplicates()

        #df_aux = self.df

        #max_temp = df_aux.loc[df_aux['temp'].idxmax()]
        #min_temp = df_aux.loc[df_aux['temp'].idxmin()]    

        #print(max_temp, "max temp es")

        for index, row in df_max_min.iterrows():
            if row['isdaylight']:            
                x_axis = row['time'].split("+")

                #This code is for adding the sun time
                fig.add_vrect(x0=x_axis[0], x1=x_axis[1], row="all", col=1,
                        annotation_text="", annotation_position="top left",
                        fillcolor="yellow", opacity=0.25, line_width=0.2)
                
        

    def fill_precipitation_subplot() -> None:
        '''
        Fills the precipitation subplot using the dataframe
        :rtype: None
        '''
        pass
    
    def fill_wind_subplot(self) -> None:
        '''
        Fills the wind subplot using the dataframe
        :rtype: None
        '''
        df = self.df
        fig = self.fig        
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

    def update_layout(self) -> None:
        '''
        Updates the layout of the dashboard it should be used at the end to not override
        the layout.
        :rtype: None
        '''

        self.fig.update_layout(title_text="LCO <br><sup>20.01°S / 70.69°W (2365m asl)</sup>",
                        font_size = 15,
                        height=700,
                        showlegend = True,
                        paper_bgcolor = "rgb(223, 223, 223)",
                        autotypenumbers='convert types')
        
    def generate_dash(self) -> None:
        '''
        Generates the dashboard using every previous method, class must be instantiated.
        :rtype: None
        '''
        self.create_subplots()
        self.fill_wind_subplot() # For some reason wind subplot must be first ? 
        self.fill_temperature_subplot()
        self.update_layout()
        