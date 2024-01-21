import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
from lcodataclient import dataclient
from datetime import datetime, timedelta
import logging
import os

import plotly.express as px


logging.basicConfig(filename='logs.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



class VaisalaDashBoard():
    '''Class for Vaisala Dashboard'''
    def __init__(self, station) -> None:
        '''
        Init instance.
        :rtype: None
        '''
        v = dataclient.VaisalaData.parameters(station = station,
                                              start_ts = '2024-01-04 14:00:00',                                                                  
                                              limit = '1440')

        data = dataclient.DataService.get(v)

        self.df = data
        self.fig = None #This is the plotly figure to display

    def create_subplots(self) -> None:
        '''
        Creates a subplot with 3 rows and 2 columns, the 3 rows in the first 
        column are used to display: Pressure, Wind and Temperature. The 2nd row
        is for displaying the winddirectionn using a rowspan=3. 
        :rtype: None
        '''
        df = self.df

        
        df.sort_index(inplace=True)

        df['time'] = df.index

        df.dropna(subset=['temperature'], inplace=True)

        fig = make_subplots(rows=3, 
                            cols=2,
                            shared_xaxes=True,
                            vertical_spacing=0,                    
                        specs=[[{"type": "xy", "secondary_y": True}, {"type": "polar", "rowspan": 3}],
                              [{"type": "xy"}, {"type": "polar"}],
                              [{"type": "xy", "secondary_y": True}, {"type": "polar"}]],)
        
        
        # Temperature plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['temperature'], 
                                 name="Temperature"),
                                 row=1,
                                 col=1,
                                 secondary_y=False)
        
        # Humidity plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['relative_humidity'], 
                                 name="Humidity"),
                                 row=1,
                                 col=1,
                                 secondary_y=True)

        # Wind plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_avg'], 
                                 name="Wind"),
                                 row=2, 
                                 col=1)
        
        # Air Pressure plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['air_pressure'], 
                                 name="Pressure"),                                
                                 secondary_y=False,
                                 row=3, 
                                 col=1)
    
        # Wind Minimum plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_min'], 
                                 name="WindMin"),
                                 row=2, 
                                 col=1)
        
        # Wind Maximum plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_max'], 
                                 name="WindMax"),
                                 row=2, 
                                 col=1)
        
        # Wind average direction plot
        fig.add_trace(go.Scatterpolargl(r = df.wind_speed_avg,
                                        theta = df.wind_dir_avg,
                                        name = "Wind AVG",
                                        mode = "markers",
                                        marker=dict(size=15, 
                                                    color="mediumseagreen")      
                                        ),row=1,
                                        col=2)
        
        # Wind minimum direction plot
        fig.add_trace(go.Scatterpolargl(r = df.wind_speed_min,
                                        theta = df.wind_dir_min,
                                        name = "Wind MIN",
                                        mode = "markers",
                                        marker=dict(size=20, 
                                                    color="gold", 
                                                    opacity=0.7)      
                                        ),row=1,
                                        col=2)
        
        # Wind maximum direction plot
        fig.add_trace(go.Scatterpolargl(r = df.wind_speed_max,
                                        theta = df.wind_dir_max,
                                        name = "Wind MAX",
                                        mode="markers",
                                        marker=dict(size=12, 
                                                    color="red", 
                                                    opacity=0.7)      
                                        ),row=1,
                                        col=2)

        # y-axis text layout
        fig.update_yaxes(title_text="Temperature[°C]",
                         secondary_y=False,
                         row=1,
                         col=1)
        
        fig.update_yaxes(title_text="Humidity[%]",
                         secondary_y=True,
                         row=1,
                         col=1)

        fig.update_yaxes(title_text="Wind[Mph]",
                         row=2,
                         col=1)
        
        fig.update_yaxes(title_text="Pressure[mb]",
                         secondary_y=False,
                         row=3,
                         col=1)
        
        #TODO: Find the values to place the text at the right side of the plot
        fig.add_annotation(dict(x=0.39, y=0.3, ax=5, ay=0,
                            xref = "paper", 
                            yref = "paper", 
                            text= "Sun Event: HH:MM - Twilight: HH:MM"),
                            textangle=-90,)

        self.fig = fig

    def fill_pressure_subplot(self) -> None:
        '''
        Fills pressure subplot using the dataframe.
        :rtype: None
        '''
        pass

    def fill_wind_subplot(self) -> None:
        '''
        Fills wind subplot using the dataframe.
        :rtype: None
        '''
        pass

    def fill_temperature_subplot(self) -> None:
        '''
        Fills temperature subplot using the dataframe.
        :rtype: None
        '''
        pass

    def fill_winddirection_subplot(self) -> None:
        '''
        Fills winddirection subplot using the dataframe.
        :rtype: None
        '''
        pass

    def update_layout(self) -> None:
        '''
        Updates the layout of the dashboard it should be used at the end to not 
        override the layout.
        :rtype: None
        '''
        now = datetime.now() - timedelta(days=1)

        now_string = now.strftime("%Y-%m-%d  %H:%M:%S")
        
        self.fig.update_layout(title_text=now_string,
                                font_size = 15, 
                                height=700,
                                autotypenumbers='convert types',
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

    def generate_dash(self) -> None:
        '''
        Generates the dashboard using every previous method, class must be 
        instantiated.
        :rtype: None
        '''

        self.create_subplots()
        self.update_layout()        
        '''
        try: 
            self.create_subplots()
            logging.info('Vaisala subplot created correctly')
        except:
            logging.error('Couldnt create Vaisala Subplots')            

        try: 
            self.update_layout()
            logging.info('Vaisala layout updated correctly')
        except:
            logging.error('Couldnt update Vaisala layout')
        '''    


class MeteoBlueDashboard():
    '''Class for MeteoBlue Dashboard generation'''

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
        Creates a subplot with 3 scatter plots to display Temperature, 
        Precipitation, Wind and WindDirection.
        :rtype = None
        '''
        df = self.df
        #The x-axis needs to be sorted otherwise the plot will not work properly
        df.sort_index(inplace=True)

        df['time'] = df.index

        df.dropna(subset=['temp'], inplace=True)

        fig = make_subplots(rows=3, 
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.02,                    
                            specs=[[{"type": "xy"}],
                                  [{"type": "xy", "secondary_y": True}],
                                  [{"type": "xy"}]],)
        
        
        # Temperature plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['temp'], 
                                 name="Temperature"),
                                 row=1, 
                                 col=1)

        # Precipitation plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['precipitation_probability'], 
                                 name="Precipitation"),
                                 row=2, 
                                 col=1)
        
        # Wind plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['windspeed'], 
                                 name="Wind"),
                                 row=3, 
                                 col=1)
        
        # Shows the name of the graph in y-axis
        fig['layout']['yaxis']['title']='Temperature <br> °C'
        #fig['layout']['yaxis2']['title']='Precipitation'
        fig['layout']['yaxis3']['title']='(km/h)'

        # Adds a dash line for the actual time
        now = datetime.now()

        now_string = now.strftime("%Y-%m-%d %H:%M:%S")    

        # Displays the line
        fig.add_vline(x=now_string, 
                      line_width=3, 
                      line_dash="dash", 
                      line_color="black")

        self.fig = fig

    def fill_temperature_subplot(self) -> None:
        '''
        Fills temperature subplot using the dataframe.
        TODO: Fix the dataframe changing after using df.update()
        :rtype: None
        '''

        df= self.df
        fig = self.fig

        df['time_aux'] = df['time']
        # Following code explanation
        # check: https://stackoverflow.com/questions/63731256/how-to-show-ranges-of-repeated-values-in-a-colum-in-python-pandas
        (df.update((df.astype(str)).groupby((df.isdaylight!=df.isdaylight.shift())\
        .cumsum())["time"].transform(lambda x: x.iloc[0]+'+'+x.iloc[-1])))
        df = df[['isdaylight', 'time']]
        df = df.drop_duplicates()

        #TODO: find a way to not use df['time_aux']
        max_temp = self.df.loc[self.df['temp'].idxmax()]
        min_temp = self.df.loc[self.df['temp'].idxmin()]    

        #print(max_temp, "max temp es")

        for index, row in df.iterrows():
            if row['isdaylight']:            
                x_axis = row['time'].split("+")
                
                #This code is for adding the sun time
                fig.add_vrect(x0=x_axis[0], x1=x_axis[1], row="all", col=1,
                        annotation_text="", annotation_position="top left",
                        fillcolor="yellow", opacity=0.25, line_width=0.2)
                #Adds the maximum value for temperature
                fig.add_annotation(x=max_temp['time_aux'],
                                y=max_temp['temp'],
                                text=max_temp['temp'],
                                showarrow=True,
                                row=1,
                                col=1)
                #Adds the minimum value for temperature
                fig.add_annotation(x=min_temp['time_aux'],
                                y=min_temp['temp'],
                                showarrow=True,
                                text=min_temp['temp'],
                                row=1,
                                col=1)
                
                
    def fill_precipitation_subplot(self) -> None:
        '''
        Fills the precipitation subplot using the dataframe
        :rtype: None
        '''
        self.fig.add_hrect(y0=0, 
                           y1=1.2, 
                           row=2, 
                           col=1,                    
                           fillcolor="brown", 
                           opacity=0.65, 
                           line_width=0.2)
    
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
        Updates the layout of the dashboard it should be used at the end to not 
        override the layout.
        :rtype: None
        '''

        # y-axis text layout
        self.fig.update_yaxes(title_text="Precipitation <br> (mm)",
                         secondary_y=False,
                         range=[0, 5],
                         row=2,
                         col=1)
        
        # y-axis text layout
        self.fig.update_yaxes(title_text="(km/h)",
                         secondary_y=False,
                         row=2,
                         col=1)

        self.fig.update_layout(title_text="LCO <br><sup>20.01°S / 70.69°W (2365m asl)</sup>",
                               font_size = 15,
                               height=700,
                               showlegend = True,
                               paper_bgcolor = "rgb(223, 223, 223)",
                               autotypenumbers='convert types')
        
    def generate_dash(self) -> None:
        '''
        Generates the dashboard using every previous method, class must be 
        instantiated.
        :rtype: None
        '''
        
        self.create_subplots()
        self.fill_wind_subplot() # For some reason wind subplot must be first ? 
        self.fill_precipitation_subplot()
        self.fill_temperature_subplot()
        self.update_layout()
        
        '''
        try: 
            self.create_subplots()
            logging.info('MeteoBlue subplot created correctly')
        except:
            logging.error('Couldnt create MeteoBlue Subplots')
        
        try: 
            self.fill_temperature_subplot()
            logging.info('MeteoBlue temperature subplot filled correctly')
        except:
            logging.error('Couldnt fill Meteoblue temperature subplot correctly')

        try: 
            self.fill_wind_subplot() # For some reason wind subplot must be first ? 
            logging.info('MeteoBlue wind plot filled correctly')
        except:
            logging.error('Couldnt fill Meteoblue wind subplot correctly')

        try: 
            self.update_layout()
            logging.info('MeteoBlue layout updated correctly')
        except:
            logging.error('Couldnt update Meteoblue layout')
        '''    


class Dummyrender():
    def __init__(self, station) -> None:
        '''
        Init instance.
        :rtype: None
        '''

        if station == "Magellan":
            print(os.getcwd())
            data = pd.read_csv("dashboards/Dash_Apps/test_data/magellandf.csv")

            self.df = data
            self.fig = None #This is the plotly figure to display
            self.fig_seeing = None
            self.fig_scattergl = None

        if station == "DuPont":
            data = pd.read_csv("dashboards/Dash_Apps/test_data/dupontdf.csv")

            self.df = data
            self.fig = None #This is the plotly figure to display
            self.fig_seeing = None
            self.fig_scattergl = None

        if station == "C40":
            data = pd.read_csv("dashboards/Dash_Apps/test_data/c40df.csv")

            self.df = data
            self.fig = None #This is the plotly figure to display
            self.fig_seeing = None
            self.fig_scattergl = None

    def generate_dash(self) -> None:

        df = self.df

        # DewPoint column calculation
        df['dp'] = df['temperature'] - ((100 - df['relative_humidity']) / 5)
        
        df.sort_index(inplace=True)

        df.dropna(subset=['temperature'], inplace=True)

        fig = make_subplots(rows=3, 
                            cols=2,
                            shared_xaxes=True,
                            vertical_spacing=0,                    
                        specs=[[{"type": "xy", "secondary_y": True}, {"type": "polar", "rowspan": 2}],
                              [{"type": "xy"}, {"type": "polar"}],
                              [{"type": "xy"}, {"type": "xy"}]],)
        
        
        # Temperature plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['temperature'], 
                                 line=dict(color="red"),
                                 name="Temperature"),
                                 row=1,
                                 col=1,
                                 secondary_y=False)
        
        # Dew Point
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['dp'], 
                                 line=dict(color="purple"),
                                 name="DewPoint"),
                                 row=1,
                                 col=1,
                                 secondary_y=False)

        
        
        # Humidity plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['relative_humidity'],
                                 line=dict(color="blue"), 
                                 name="Humidity"),
                                 row=1,
                                 col=1,
                                 secondary_y=True)

        # Wind plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_avg'], 
                                 line=dict(color="green"),
                                 name="Wind"),
                                 row=2, 
                                 col=1)
        
        # Air Pressure plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['temperature'], 
                                 line=dict(color="black"),
                                 name="Pressure"),                                                                 
                                 row=3, 
                                 col=1)
    
        # Wind Minimum plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_min'], 
                                 line=dict(color="green"),
                                 name="WindMin"),
                                 row=2, 
                                 col=1)
        
        # Wind Maximum plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_max'], 
                                 line=dict(color="lightgreen"),
                                 name="WindMax"),
                                 row=2, 
                                 col=1)

        
        #This code is useful for creating the vertical lines for sunrise and sunset
        sunrise_event = "2024-01-05 07:00:00"
        sunset_event = "2024-01-06 21:00:00"

    
        # Displays the line for Sunrise
        fig.add_vline(x=sunrise_event, 
                      line_width=3,                       
                      line_color="grey",
                      col=1)

        # Displays the line for Sunset
        fig.add_vline(x=sunset_event, 
                      line_width=3,                        
                      line_color="grey",
                      col=1)                                  
        
        # Wind average direction plot
        fig.add_trace(go.Scatterpolargl(r = df.wind_speed_avg,
                                        theta = df.wind_dir_avg,
                                        name = "Wind AVG",
                                        mode = "markers",
                                        marker=dict(size=5, 
                                                    color="mediumseagreen")      
                                        ),row=1,
                                        col=2)
        
        # Wind minimum direction plot
        fig.add_trace(go.Scatterpolargl(r = df.wind_speed_min,
                                        theta = df.wind_dir_min,
                                        name = "Wind MIN", 
                                        mode = "markers",
                                        marker=dict(size=7, 
                                                    color="lightgreen", 
                                                    opacity=0.7)      
                                        ),row=1,
                                        col=2)
        
        # Wind maximum direction plot
        fig.add_trace(go.Scatterpolargl(r = df.wind_speed_max,
                                        theta = df.wind_dir_max,
                                        name = "Wind MAX",
                                        mode="markers",
                                        marker=dict(size=8, 
                                                    color="green", 
                                                    opacity=0.7)      
                                        ),row=1,
                                        col=2)

        # Seeing plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['temperature'], 
                                 line=dict(color="red"),
                                 name="Temperature"),
                                 row=3,
                                 col=2,
                                 secondary_y=False)                                               

        # y-axis text layout
        fig.update_yaxes(title_text="DP, Temperature[°C]",
                         secondary_y=False,
                         range=[-40, 40],
                         row=1,
                         col=1)
        
        fig.update_yaxes(title_text="Humidity[%]",
                         secondary_y=True,
                         range=[0, 100],
                         row=1,
                         col=1)

        fig.update_yaxes(title_text="Wind[Mph]",
                         range=[0, 50],
                         row=2,
                         col=1)
        
        fig.update_yaxes(title_text="Pressure[mb]",                         
                         row=3,
                         col=1)

        fig.update_yaxes(title_text="Seeing",                         
                         row=3,
                         col=2)     
        
        
        #TODO: Find the values to place the text at the right side of the plot
        fig.add_annotation(dict(x=0.39, y=0.3, ax=5, ay=0,
                            xref = "paper", 
                            yref = "paper", 
                            text= f'Sun Event: {sunrise_event[11:16]} - Twilight: {sunset_event[11:16]}'),
                            textangle=-90,)
        #eye
        self.fig = fig

        now = datetime.now() - timedelta(days=1)

        now_string = now.strftime("%Y-%m-%d  %H:%M:%S")
        
        self.fig.update_layout(title_text=now_string,
                                font_size = 15, 
                                height=700,
                                autotypenumbers='convert types',
                                showlegend = False,
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

    def generate_seeing_plot(self) -> None:
        df = self.df

        df.sort_index(inplace=True)

        df.dropna(subset=['temperature'], inplace=True)

        self.fig_seeing = px.scatter(df, x=df['time'], y=df['temperature'])
        self.fig_seeing.update_layout(showlegend=False, 
                                      height=200,
                                      paper_bgcolor = "rgb(223, 223, 223)")

    def generate_stations_plot(self) -> None:
        df = self.df

        # DewPoint column calculation
        df['dp'] = df['temperature'] - ((100 - df['relative_humidity']) / 5)
        
        df.sort_index(inplace=True)

        df.dropna(subset=['temperature'], inplace=True)

        fig = make_subplots(rows=3, 
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0,                    
                        specs=[[{"type": "xy", "secondary_y": True}],
                              [{"type": "xy"}],
                              [{"type": "xy"}]],)
        
        
        # Temperature plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['temperature'], 
                                 line=dict(color="red"),
                                 name="Temperature"),
                                 row=1,
                                 col=1,
                                 secondary_y=False)
        
        # Dew Point
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['dp'], 
                                 line=dict(color="purple"),
                                 name="DewPoint"),
                                 row=1,
                                 col=1,
                                 secondary_y=False)

        
        
        # Humidity plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['relative_humidity'],
                                 line=dict(color="blue"), 
                                 name="Humidity"),
                                 row=1,
                                 col=1,
                                 secondary_y=True)

        # Wind plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_avg'], 
                                 line=dict(color="green"),
                                 name="Wind"),
                                 row=2, 
                                 col=1)
        
        # Air Pressure plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['temperature'], 
                                 line=dict(color="black"),
                                 name="Pressure"),                                                                 
                                 row=3, 
                                 col=1)
    
        # Wind Minimum plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_min'], 
                                 line=dict(color="green"),
                                 name="WindMin"),
                                 row=2, 
                                 col=1)
        
        # Wind Maximum plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_max'], 
                                 line=dict(color="lightgreen"),
                                 name="WindMax"),
                                 row=2, 
                                 col=1)

        
        #This code is useful for creating the vertical lines for sunrise and sunset
        sunrise_event = "2024-01-05 07:00:00"
        sunset_event = "2024-01-06 21:00:00"

    
        # Displays the line for Sunrise
        fig.add_vline(x=sunrise_event, 
                      line_width=3,                       
                      line_color="grey",
                      col=1)

        # Displays the line for Sunset
        fig.add_vline(x=sunset_event, 
                      line_width=3,                        
                      line_color="grey",
                      col=1)                                                                           

        # y-axis text layout
        fig.update_yaxes(title_text="DP, Temperature[°C]",
                         secondary_y=False,
                         range=[-40, 40],
                         row=1,
                         col=1)
        
        fig.update_yaxes(title_text="Humidity[%]",
                         secondary_y=True,
                         range=[0, 100],
                         row=1,
                         col=1)

        fig.update_yaxes(title_text="Wind[Mph]",
                         range=[0, 50],
                         row=2,
                         col=1)
        
        fig.update_yaxes(title_text="Pressure[mb]",                         
                         row=3,
                         col=1)
        
        
        #TODO: Find the values to place the text at the right side of the plot
        fig.add_annotation(dict(x=0.99, y=0.3, ax=5, ay=0,
                            xref = "paper", 
                            yref = "paper", 
                            text= f'Sun Event: {sunrise_event[11:16]} - Twilight: {sunset_event[11:16]}'),
                            textangle=-90,
                            font_size=13)
        #eye
        self.fig = fig

        now = datetime.now() - timedelta(days=1)

        now_string = now.strftime("%Y-%m-%d  %H:%M:%S")
        
        self.fig.update_layout( font_size = 10, 
                                height=500,                                
                                autotypenumbers='convert types',
                                showlegend = False,                                
                                paper_bgcolor = "rgb(223, 223, 223)")

    def generate_scattergl_plot(self) -> None:
        df = self.df        
        
        df.sort_index(inplace=True)

        df.dropna(subset=['temperature'], inplace=True)

        self.fig_scattergl = go.Figure()

        # Wind average direction plot
        self.fig_scattergl.add_trace(go.Scatterpolargl(r = df.wind_speed_avg,
                                        theta = df.wind_dir_avg,
                                        name = "Wind AVG",
                                        mode = "markers",
                                        marker=dict(size=5, 
                                                    color="mediumseagreen")      
                                        ))
        
        # Wind minimum direction plot
        self.fig_scattergl.add_trace(go.Scatterpolargl(r = df.wind_speed_min,
                                        theta = df.wind_dir_min,
                                        name = "Wind MIN", 
                                        mode = "markers",
                                        marker=dict(size=7, 
                                                    color="lightgreen", 
                                                    opacity=0.7)      
                                        ))
        
        # Wind maximum direction plot
        self.fig_scattergl.add_trace(go.Scatterpolargl(r = df.wind_speed_max,
                                        theta = df.wind_dir_max,
                                        name = "Wind MAX",
                                        mode="markers",
                                        marker=dict(size=8, 
                                                    color="green", 
                                                    opacity=0.7)      
                                        ))

        self.fig_scattergl.update_layout(
                                font_size = 15,                                 
                                height=340,
                                autotypenumbers='convert types',
                                showlegend = False,
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
