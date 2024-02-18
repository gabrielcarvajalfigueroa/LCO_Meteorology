import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
from lcodataclient import dataclient
from datetime import datetime, timedelta
import logging
from numpy import log as ln
import ephem

import plotly.express as px

'''
logging.basicConfig(filename='logsg.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
'''


class VaisalaDashBoard():
    '''Class for Vaisala Dashboard'''
    def __init__(self, station, history_start=None, history_end=None) -> None:
        '''
        Init instance.
        :rtype: None
        '''
        self.station = station
        self.fig = None #This is the plotly figure to display
        self.fig_seeing = None
        self.fig_scattergl = None
        self.history_start = history_start #This attribute is used to check the live or history display

        if history_start == None:

            now = datetime.now() - timedelta(days=1)

            now_string = now.strftime("%Y-%m-%d %H:%M:%S")
            v = dataclient.VaisalaData.parameters(station = station,
                                                start_ts = now_string,  
                                                limit = '1440')

            data = dataclient.DataService.get(v)

            data['time'] = data.index

            # Converts pressure from inHg to mb
            data['air_pressure'] = data['air_pressure'] * 33.864

            # Sorts the data by the timestamp which is the index
            data.sort_index(inplace=True)
            
            self.df = data        

        else:
            
            v = dataclient.VaisalaData.parameters(station = station,
                                                start_ts = history_start,  
                                                end_ts = history_end,
                                                limit = '1440')

            data = dataclient.DataService.get(v)

            data['time'] = data.index

            # Converts pressure from inHg to mb
            data['air_pressure'] = data['air_pressure'] * 33.864

            # Sorts the data by the timestamp which is the index
            data.sort_index(inplace=True)

            self.df = data            
            
    def get_ephems(self) -> list:
        '''
        Uses ephem library to obtain dates for sunset, twilightend,
        twilightbegin and sunrise. 
        
        And also returns the next sunevent and twilight
        to display in the graph. 

        All of the data is returned in a list with the following order
        considering that the list is called ephem.

        ephem[0]: sunset
        ephem[1]: twiend
        ephem[2]: twibeg
        ephem[3]: sunrise
        ephem[4]: sun_event
        ephem[5]: twi_event

        :rtype: list
        '''

        '''
        [LCO]
        Latitude:-29.0110777
        Longitude:-70.700561
        Elevation:2274
        Horizon:-1.4
        TWL_Horizon:-18
        Pressure:760
        '''
        now = datetime.now()

        LCO = ephem.Observer()
        LCO.lat = "-29.0110777"
        LCO.lon = "-70.700561"
        LCO.elevation = 2274
        LCO.horizon = "-1.4"
        LCO.pressure = float("760")
        
        if int(now.strftime("%H")) >= 16:
            LCO.date = datetime.now()  
        else:
            LCO.date = datetime.now() - timedelta(days=1)

        
        sun = ephem.Sun()
        sunrise = ephem.localtime(LCO.next_rising(sun))
        sunset = ephem.localtime(LCO.next_setting(sun))
        LCO.horizon = "-18"
        twibeg = ephem.localtime(LCO.next_rising(sun))
        twiend = ephem.localtime(LCO.next_setting(sun))            

        # -----------------------------------------------------
        # Ephem string calculation: Do we plot old data or next?
        # -----------------------------------------------------
        
        isDay = False
        isTwi = False

        if sunset > now:
            isDay = True        
            sunset = sunset - timedelta(days=1)    

        if sunrise > now:
            sunrise = sunrise - timedelta(days=1)
        else:
            isDay = True
        
        if twibeg > now:
            twibeg = twibeg - timedelta(days=1)
        
        if twiend > now:
            isDay = False
            #isTwi = True
            twiend = twiend - timedelta(days=1)

        if isDay:
            sun_event = sunset.strftime('%H:%M')
            twi_event = twiend.strftime('%H:%M')

        else:
            if isTwi:
                sun_event = sunrise.strftime('%H:%M')
                twi_event = twiend.strftime('%H:%M')

            else:
                sun_event = sunrise.strftime('%H:%M')
                twi_event = twibeg.strftime('%H:%M')

        sunrise_str = sunrise.strftime('%Y-%m-%d %H:%M:%S')
        sunset_str = sunset.strftime('%Y-%m-%d %H:%M:%S')
        twibeg_str = twibeg.strftime('%Y-%m-%d %H:%M:%S')
        twiend_str = twiend.strftime('%Y-%m-%d %H:%M:%S')                    
        
        return [sunset_str, twiend_str, twibeg_str, sunrise_str, sun_event, twi_event]

    def generate_seeing_plot(self) -> None:
        df = self.df

        self.fig_seeing = px.line(df, x=df['time'], y=df['temperature'])

        self.fig_seeing.update_yaxes(title_text="seeing")
        
        self.fig_seeing.update_xaxes(title_text="")
        
        self.fig_seeing.update_traces(line=dict(color="green", width=0.5))

        self.fig_seeing.update_layout(showlegend=False, 
                                      height=200,
                                      margin=dict(t=35),
                                      paper_bgcolor = "rgb(223, 223, 223)")

    def generate_stations_plot(self) -> None:
        df = self.df

        # DewPoint column calculation 
        # trh = (((17.27 * df['temperature'])/(273.7 + df['temperature'])) + ln(0.01 * df['relative_humidity']))
        # dewpoint = (237.7*trh)/(17.27-trh)
        df['dp'] = (237.7*(((17.27 * df['temperature'])/(273.7 + df['temperature'])) + ln(0.01 * df['relative_humidity'])))/(17.27-(((17.27 * df['temperature'])/(273.7 + df['temperature'])) + ln(0.01 * df['relative_humidity'])))                

        self.fig = make_subplots(rows=3, 
                                 cols=1,
                                 shared_xaxes=True,
                                 vertical_spacing=0,                    
                                 specs=[[{"type": "xy", "secondary_y": True}],
                                    [{"type": "xy"}],
                                    [{"type": "xy"}]],)
                
        # Temperature plot
        self.fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['temperature'], 
                                 line=dict(color="red", width=1),
                                 name="Temperature"),
                                 row=1,
                                 col=1,
                                 secondary_y=False)
        
        # Dew Point
        self.fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['dp'], 
                                 line=dict(color="purple", width=1),
                                 name="DewPoint"),
                                 row=1,
                                 col=1,
                                 secondary_y=False)
            
        # Humidity plot
        self.fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['relative_humidity'],
                                 line=dict(color="blue", width=1), 
                                 name="Humidity"),
                                 row=1,
                                 col=1,
                                 secondary_y=True)
        
        # This H-line is for defining a limit for humidity
        # This limit is the one used for warnings below: 80%
        self.fig.add_hline(y=80, 
                      line_width=2, 
                      line_dash="dash", 
                      line_color="red",
                      secondary_y=True,
                      opacity= 0.4,
                      row=1,
                      col=1)            
        
        # Wind plot
        self.fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_avg'], 
                                 line=dict(color="green", width=1),
                                 name="Wind"),
                                 row=2, 
                                 col=1)
        
        # This H-line is for defining a limit for Wind speed
        # This limit is the one used for warnings below: 35 km/h
        self.fig.add_hline(y=35, 
                      line_width=2, 
                      line_dash="dash", 
                      line_color="red",
                      opacity= 0.4,
                      row=2,
                      col=1)
        
        # Air Pressure plot
        self.fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['air_pressure'], 
                                 line=dict(color="black", width=1),
                                 name="Pressure"),                                                                 
                                 row=3, 
                                 col=1)
    
        # Wind Minimum plot
        self.fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_min'], 
                                 line=dict(color="green", width=1),
                                 name="WindMin"),
                                 row=2, 
                                 col=1)
        
        # Wind Maximum plot
        self.fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['wind_speed_max'], 
                                 line=dict(color="lightgreen", width=1),
                                 name="WindMax"),
                                 row=2, 
                                 col=1)

        # y-axis text layout
        self.fig.update_yaxes(title_text="DP, Temperature[°C]",
                         secondary_y=False,
                         range=[-40, 40],
                         row=1,
                         col=1)
        
        self.fig.update_yaxes(title_text="Humidity[%]",
                         secondary_y=True,
                         range=[0, 100],
                         row=1,
                         col=1)

        self.fig.update_yaxes(title_text="Wind[Mph]",
                         range=[0, 60],
                         row=2,
                         col=1)
        
        # Magellan handles different pressure values compared to Dupont and C40 
        # who share the same values.
        if self.station == "Magellan":
            self.fig.update_yaxes(title_text="Pressure[mb]",
                            range=[756, 770],
                            row=3,
                            col=1)        
        else:
            self.fig.update_yaxes(title_text="Pressure[mb]",
                            range=[766, 780],
                            row=3,
                            col=1)

        # This if, is used because when plotting history data the things that are
        # below are not neccesary        
        if self.history_start == None:
            
            # ----------------------------
            # Latest and average variables
            # ----------------------------

            latest_temp = round(df['temperature'].iloc[-1], 1)
            latest_humidity = round(df['relative_humidity'].iloc[-1], 1)
            latest_dewpoint = round(df['dp'].iloc[-1], 1)
            latest_wind = round(df['wind_speed_avg'].iloc[-1], 1)
            latest_gust = round(df['wind_speed_max'].iloc[-1], 1)

            avg_temp = round(df['temperature'].mean(), 1)
            avg_humidity = round(df['relative_humidity'].mean(), 1)
            avg_dewpoint = round(df['dp'].mean(), 1)
            avg_wind = round(df['wind_speed_avg'].mean(), 1)

            now_hour = datetime.now()
            now_hour_string = now_hour.strftime("%H:%M:%S")


            # Annotation for current time latest(average)
            self.fig.add_annotation(text=f"{now_hour_string}",
                                xref="paper", 
                                yref="paper",
                                x=0.48, 
                                y=0.99,
                                font_size=15,
                                font_color="grey",
                                showarrow=False)

            # Annotation for temperature latest(average)
            self.fig.add_annotation(text=f"{latest_temp}({avg_temp})",
                                xref="paper", 
                                yref="paper",
                                x=0, 
                                y=1,
                                font_size=20,
                                font_color="red",
                                showarrow=False)
            
            # Annotation for Humidity latest(average)
            self.fig.add_annotation(text=f"{latest_humidity}({avg_humidity})",
                                xref="paper", 
                                yref="paper",
                                x=0.93, 
                                y=1,
                                font_size=20,
                                font_color="blue",
                                showarrow=False)
            
            # Annotation for DewPoint latest(average)
            self.fig.add_annotation(text=f"{latest_dewpoint}({avg_dewpoint})",
                                xref="paper", 
                                yref="paper",
                                x=0, 
                                y=0.8,
                                font_size=20,
                                font_color="purple",
                                showarrow=False)
            
            # Annotation for Latest Gust
            self.fig.add_annotation(text=f"Gusts: {latest_gust}",
                                xref="paper", 
                                yref="paper",
                                x=0, 
                                y=0.68,
                                font_size=14,
                                font_color="gray",
                                showarrow=False)
            
            # Annotation for Wind latest(average)
            self.fig.add_annotation(text=f"{latest_wind}({avg_wind})",
                                xref="paper", 
                                yref="paper",
                                x=0, 
                                y=0.6,
                                font_size=20,
                                font_color="green",
                                showarrow=False)
            
            # -------------------------------
            #       Lines for ephemeris
            # -------------------------------
        
            ephems = self.get_ephems()

            # Line for sunset (lightblue)

            self.fig.add_vline(x=ephems[0], 
                        line_width=3,
                        opacity=0.3,
                        line_color="lightblue")

            # Line for twilight end (gray)

            self.fig.add_vline(x=ephems[1], 
                        line_width=3,
                        opacity=0.3,
                        line_color="gray")

            # Line for twilight begin (gray)

            self.fig.add_vline(x=ephems[2], 
                        line_width=3,
                        opacity=0.3,
                        line_color="gray")

            # Line for sunrise (lightblue)

            self.fig.add_vline(x=ephems[3], 
                        line_width=3,
                        opacity=0.3,
                        line_color="lightblue")
            
            # Annotation for Sun event and Twilight
            self.fig.add_annotation(dict(x=0.99, y=0.3, ax=5, ay=0,
                                xref = "paper", 
                                yref = "paper", 
                                text= f'Sun Event: {ephems[4]} - Twilight: {ephems[5]}'), 
                                textangle=-90,
                                font_size=13)

            # -------------------------------
            #   Line for half an hour ago
            # -------------------------------

            half_hour = now_hour - timedelta(minutes=30)
            self.fig.add_vline(x=half_hour.strftime("%Y-%m-%d %H:%M:%S"), 
                        line_width=3,   
                        opacity=0.3,
                        line_color="magenta")

            # ----------------------------------
            #  Warnings for certain conditions
            # ----------------------------------
            # This warnings are displayed in the same x value only y changes.
            # - High wind: If last wind speed is >= 35
            # - High Humidity: If last humidity is >= 80
            # - Danger of Precipitation: If |last_temperature - last_dewpoint)| < 2.0

            if latest_wind >= 35:
                self.fig.add_annotation(text="Note: High Wind",
                                    xref="paper", 
                                    yref="paper",
                                    x=0.5, 
                                    y=0,
                                    font_size=20,
                                    font_color="gray",
                                    showarrow=False)
            
            if latest_humidity >= 80:            
                self.fig.add_annotation(text="Note: High Humidity",
                                    xref="paper", 
                                    yref="paper",
                                    x=0.5, 
                                    y=0.1,
                                    font_size=20,
                                    font_color="gray",
                                    showarrow=False)

            if abs(latest_temp - latest_dewpoint) < 2.0:            
                self.fig.add_annotation(text="Note: Danger of Precipitation",
                                    xref="paper", 
                                    yref="paper",
                                    x=0.5, 
                                    y=0.7,
                                    font_size=20,
                                    font_color="gray",
                                    showarrow=False)

        else:
            # Annotation for history time, displays the day selected to plot
            # eg. 2024-02-16
            self.fig.add_annotation(text=self.history_start[:10],
                                xref="paper", 
                                yref="paper",
                                x=0.48, 
                                y=0.99,
                                font_size=15,
                                font_color="grey",
                                showarrow=False)            
        
        # Updates layout for stations figure
        self.fig.update_layout( font_size = 10, 
                                height=500,
                                margin=dict(l=20, r=20, t=20, b=20),
                                autotypenumbers='convert types',
                                showlegend = False,                                
                                paper_bgcolor = "rgb(223, 223, 223)")

    def generate_scattergl_plot(self) -> None:

        self.fig_scattergl = go.Figure()

        # the tail function obtains the last rows from a dataframe
        # To display the latest data
        last_100_rows = self.df.tail(100)        

        # Wind average direction plot
        self.fig_scattergl.add_trace(go.Scatterpolargl(r = last_100_rows.wind_speed_avg,
                                        theta = last_100_rows.wind_dir_avg,
                                        name = "Wind AVG",
                                        mode = "markers",
                                        marker=dict(size=5, 
                                                    color="mediumseagreen")      
                                        ))
        
        # Wind minimum direction plot
        self.fig_scattergl.add_trace(go.Scatterpolargl(r = last_100_rows.wind_speed_min,
                                        theta = last_100_rows.wind_dir_min,
                                        name = "Wind MIN", 
                                        mode = "markers",
                                        marker=dict(size=7, 
                                                    color="lightgreen", 
                                                    opacity=0.7)      
                                        ))
        
        # Wind maximum direction plot
        self.fig_scattergl.add_trace(go.Scatterpolargl(r = last_100_rows.wind_speed_max,
                                        theta = last_100_rows.wind_dir_max,
                                        name = "Wind MAX",
                                        mode="markers",
                                        marker=dict(size=8, 
                                                    color="green", 
                                                    opacity=0.7)      
                                        ))

        self.fig_scattergl.update_layout(
                                font_size = 10,                                
                                height=340,
                                margin=dict(l=35, r=35, t=35, b=35),
                                autotypenumbers='convert types',
                                showlegend = False,
                                polar = dict(
                                    bgcolor = "rgb(223, 223, 223)",
                                    angularaxis = dict(
                                        linewidth = 1,
                                        direction = "clockwise",
                                        rotation = 90,
                                        showline=True,
                                        linecolor='black'
                                    ),
                                radialaxis = dict(
                                    side = "counterclockwise",
                                    angle = 65,
                                    tickangle=90,
                                    showline = False,
                                    linewidth = 1,
                                    gridcolor = "lightgray",
                                    gridwidth = 1,
                                    griddash="dash",
                                    range=[0,50]
                                )
                                ),
                                paper_bgcolor = "rgb(223, 223, 223)")
        
    
class MeteoBlueDashboard():
    '''Class for MeteoBlue Dashboard generation'''

    def __init__(self, days) -> None:
        '''
        Init instance.
        :rtype: None
        '''        
        m = dataclient.MeteoblueData.parameters(day=False)

        data = dataclient.DataService.get(m)
        
        start_ts = datetime.today()
        end_ts = start_ts + timedelta(days=int(days))

        start_ts = start_ts.strftime("%Y-%m-%d")
        end_ts = end_ts.strftime("%Y-%m-%d")

        # Filters the data depending on the days: 1, 3 or 4
        data = data.loc[(data.index >= start_ts)
                     & (data.index < end_ts)]

        self.df= data
        self.fig = None #This is the plotly figure to display

    def create_subplots(self) -> None:
        '''
        Creates a subplot with 3  plots to display Temperature, 
        Cloud Coverage, Wind and SealevelPressure with Precipitation %.
        :rtype = None
        '''
        df = self.df
        #The x-axis needs to be sorted otherwise the plot will not work properly
        df.sort_index(inplace=True)

        df['time'] = df.index

        # It is neccesary to convert to float64 the columns otherwise the dew point 
        # calculation won't work
        df['temp'] = df['temp'].astype(float)
        df['relativehumidity'] = df['relativehumidity'].astype(float)
        
        # Dew Point Column calculation
        df['dp'] = (237.7*(((17.27 * df['temp'])/(273.7 + df['temp'])) + ln(0.01 * df['relativehumidity'])))/(17.27-(((17.27 * df['temp'])/(273.7 + df['temp'])) + ln(0.01 * df['relativehumidity'])))

        fig = make_subplots(rows=4, 
                            cols=1,
                            shared_xaxes=True,
                            vertical_spacing=0.02,                    
                            specs=[[{"type": "xy", "secondary_y": True}],
                                  [{"type": "heatmap"}],
                                  [{"type": "xy"}],
                                  [{"type": "xy", "secondary_y": True}]],)
        
        # ------------------------------------
        # --------- GRAPH - 1 ----------------
        # ------------------------------------
        # Displays:
        #   - temp
        #   - felttemperature
        #   - uvindex (bar chart)
        #   - relativehumidity
        #   - dewpoint

        #Temperature
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['temp'], 
                                 line_width=1,
                                 name="Temperature"),
                                 row=1, 
                                 col=1,
                                 secondary_y=False)
        
        # Felt temperature
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['felttemperature'], 
                                 line_width=1,
                                 name="Felt Temperature"),
                                 row=1, 
                                 col=1,
                                 secondary_y=False)
        
        # Relative Humidity
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['relativehumidity'],
                                 line_width=1,
                                 line=dict(color="blue"), 
                                 name="Humidity"),
                                 row=1,
                                 col=1,
                                 secondary_y=True)
        
        # Uv Index
        fig.add_trace(go.Bar(x=df['time'], 
                                 y=df['uvindex'],                                 
                                 name="UV-Index"),
                                 row=1,
                                 col=1,
                                 secondary_y=True)
                
        # Dew Point
        fig.add_trace(go.Scatter(x=df['time'], 
                                y=df['dp'], 
                                line=dict(color="purple", width=1),
                                name="DewPoint"),
                                row=1,
                                col=1,
                                secondary_y=False)        

        # ------------------------------------
        # --------- GRAPH - 2 ----------------
        # ------------------------------------
        # Displays:
        #   - highclouds
        #   - midclouds
        #   - lowclouds        

        cloud_types = ['Low Clouds', 'Mid Clouds', 'High Clouds']
        
        z = [df['lowclouds'].tolist(), df['midclouds'].tolist(), df['highclouds'].tolist()]

        fig.add_trace(go.Heatmap(
                    z=z,
                    x=df['time'],
                    y=cloud_types,
                    showscale=False,
                    colorscale='Greys',
                    zmax=100,
                    zmin=0),
                    row=2,
                    col=1)

        # ------------------------------------
        # --------- GRAPH - 3 ----------------
        # ------------------------------------
        # Displays:
        #   - Wind plot

        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['windspeed'], 
                                 name="Wind"),
                                 row=3, 
                                 col=1)
        
        df['windspeed'] = pd.to_numeric(df['windspeed'])
        top_limit = df['windspeed'].max()
        
        #This trace is por adding the wind direction
        fig.add_trace(go.Scatter(
                    x=df['time'],
                    y=[float(top_limit) + 1] * len(df), # Displays the wind dir at the top of the graph
                    mode='markers',
                    showlegend=False,
                    line=dict(color='blue'),
                    marker=dict(
                        color='blue',
                        size=10,
                        symbol='arrow',
                        angle=df['winddirection']
                    )), 
                    row=3, 
                    col=1)
        
        # ------------------------------------
        # --------- GRAPH - 4 ----------------
        # ------------------------------------
        # Displays:
        #   - precipitation_probability
        #   - snowfraction
        #   - sealevelpressure

        # Snow Fraction Plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['snowfraction'], 
                                 line_width=1,
                                 name="Snow Fraction"),
                                 row=4, 
                                 col=1,
                                 secondary_y=False)
        
        # Precipitation probability plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['precipitation_probability'],
                                 line_width=1, 
                                 name="Precipitation %"),
                                 row=4, 
                                 col=1,
                                 secondary_y=False)
        
        

        # Precipitation probability plot
        fig.add_trace(go.Scatter(x=df['time'], 
                                 y=df['sealevelpressure'], 
                                 line_width=1,
                                 name="Sea Level Pressure"),
                                 row=4, 
                                 col=1,
                                 secondary_y=True)                
        
        # Adds a dash line for the actual time
        now = datetime.now()

        now_string = now.strftime("%Y-%m-%d %H:%M:%S")    

        # Displays the line
        fig.add_vline(x=now_string, 
                      line_width=3, 
                      line_dash="dash", 
                      line_color="black")

        self.fig = fig

    def subplot_extras(self) -> None:
        """
        This function is in charge of plotting 2 extras which are:

        1.- Min and Max for temperature per day

        2.- Plot daylight time across every graph

        Any future extra calculation needed can be added here with no problem.

        :rtype: None
        """

        df= self.df
        fig = self.fig

        # Obtains a dataframe for max and min temperature per day with their respectives indexes
        df_2 = df.groupby(pd.Grouper(freq='1D')).agg({'temp': ['min', 'idxmin', 'max', 'idxmax']}).dropna()        

        for index, row in df_2['temp'].iterrows():
            #Adds the maximum value for temperature
            fig.add_annotation(x=row['idxmax'],
                            y=row['max'] + 3 ,
                            text=row['max'],
                            showarrow=False,
                            row=1,
                            col=1)
            #Adds the minimum value for temperature
            fig.add_annotation(x=row['idxmin'],
                            y=row['min'],
                            showarrow=True,
                            text=row['min'],
                            row=1,
                            col=1)               
        
        # This algorithm obtains the start and end values for daylight per day
        # Considering that the data comes from a sorted pandas dataframe.            
        # the data for isdaylight comes like this [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0]            
            
        # Since the dataframe is sorted both of this lists are synced
        dates = df.index.tolist()
        isdaylight = df['isdaylight'].tolist()

        # O(n)
        for i in range(len(dates)):
            # if daylight is 1 can be used as True
            if isdaylight[i]:
                # if the 0 is at the previous index means that is a start point
                if isdaylight[i-1] == 0:
                    start_daylight = dates[i]

                # if the 0 is at the next index means that is an end point
                # and that both points have to be plotted
                if isdaylight[i+1] == 0:
                    end_daylight = dates[i]
                    fig.add_vrect(x0=start_daylight, 
                          x1=end_daylight, 
                          row="all", 
                          col=1,
                          annotation_text="", 
                          annotation_position="top left",
                          fillcolor="yellow", 
                          opacity=0.25, 
                          line_width=0.2)
                
    def update_layout(self) -> None:
        '''
        Updates the layout of the dashboard it should be used at the end to not 
        override the layout.
        :rtype: None
        '''
        self.fig.update_yaxes(title_text="DP,Temperature",
                         secondary_y=False,                        
                         range=[-40, 40],
                         row=1,
                         col=1)
        
        self.fig.update_yaxes(title_text="Humidity[%]",
                         secondary_y=True,
                         range=[0, 100],
                         row=1,
                         col=1)
        
        self.fig.update_yaxes(title_text="Wind[km/h]",
                         row=3,
                         col=1)
        
        self.fig.update_yaxes(title_text="Precipitation[%]",
                         row=4,
                         col=1,
                         secondary_y=False)

        self.fig.update_yaxes(title_text="[hPa]",
                         secondary_y=True,                         
                         row=4,
                         col=1)
        
        self.fig.update_layout(title_text="LCO <br><sup>20.01°S / 70.69°W (2365m asl)</sup>",
                               font_size = 15,
                               height=700,
                               showlegend = False,
                               paper_bgcolor = "rgb(223, 223, 223)",
                               autotypenumbers='convert types')
        
    def generate_dash(self) -> None:
        '''
        Generates the dashboard using every previous method, class must be 
        instantiated.
        :rtype: None
        '''
        
        self.create_subplots()    
        self.subplot_extras()
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

