from lcodataclient import dataclient
import plotly.graph_objects as go 
from plotly.offline import plot
import plotly.express as px
from plotly.subplots import make_subplots

def plotly_plot(y_axis):
    m = dataclient.VaisalaData.parameters(station = 'Magellan',
                               start_ts = '2024-01-03 11:00:00',
                               limit = '1440')

    df = dataclient.DataService.get(m)

    #print(df[['temp', 'windspeed']].head(10))
    #print(df.index.tolist())

    df['time'] = df.index

    print(df)

    fig = go.Figure([go.Scatter(x=df['time'], y=df[y_axis])])
    
    #Update layout for graph object Figure
    fig.update_layout(title_text = 'Plotly_Plot1',
                      xaxis_title = 'X_Axis',
                      yaxis_title = 'Temperature [°C]')
    

    
    
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return plotly_plot_obj

def plotly_plot_wind():

    m = dataclient.VaisalaData.parameters(station = 'Magellan',
                               start_ts = '2024-01-03 17:00:00',                                   
                               end_ts = '2024-01-04 17:00:00',
                               limit = '1440')

    df = dataclient.DataService.get(m)

    #print(df[['temp', 'windspeed']].head(10))
    #print(df.index.tolist())

    df['time'] = df.index

    print(df)

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
    
    #fig.add_trace(go.Barpolar(theta=df['wind_dir_avg'].values.tolist(), r=df['wind_speed_avg'].values.tolist()),
    #          row=1, col=2)
    
    fig.add_trace(go.Scatterpolargl(
      r = df.wind_speed_avg,
      theta = df.wind_dir_avg,
      name = "Wind AVG",
      marker=dict(size=15, color="mediumseagreen")      
    ),row=1,
      col=2)
    
    fig.add_trace(go.Scatterpolargl(
      r = df.wind_speed_min,
      theta = df.wind_dir_min,
      name = "Wind MIN",
      marker=dict(size=15, color="gold")      
    ),row=1,
      col=2)
    
    fig.add_trace(go.Scatterpolargl(
      r = df.wind_speed_max,
      theta = df.wind_dir_max,
      name = "Wind MAX",
      marker=dict(size=15, color="red")      
    ),row=1,
      col=2)


    fig['layout']['yaxis']['title']='Pressure'
    fig['layout']['yaxis2']['title']='Wind'
    fig['layout']['yaxis3']['title']='Temperature'



    fig.update_layout(title_text="Temperature, WindSpeed, Air Pressure",
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
    
    
    
    plotly_plot_obj = plot({'data': fig}, output_type='div')

    return plotly_plot_obj