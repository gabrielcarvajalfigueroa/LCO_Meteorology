import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from .dashboards_components import MeteoBlueDashboard

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

# Days to display
days = ["1 day", "3 days", "4 days"]

#Create DjangoDash application
app = DjangoDash(name='Meteoblue')

app.layout = html.Div([

                    dcc.Dropdown(
                      id = 'days',
                      options = [{'label': i, 'value': i} for i in days],
                      clearable = False,
                      value = "4 days",#Initial value for the dropdown
                      style={'width': '25%', 'margin':'0px auto'}),

                    dcc.Graph(id = 'meteoblue_plot',
                              animate = False, 
                              config = toolbar_config,
                              style={"backgroundColor": "#FFF0F5"})                                                        
                    ])

# Callback for updating stations plot
@app.callback(
               Output('meteoblue_plot', 'figure'), #id of html component
              [Input('days', 'value')]) #id of html component
              
def update_value(*args,**kwargs):
    """
    This function returns Meteoblue figure according to the days selected
    the first time renders with 4 days
    Input: days selected
    Output: Meteoblue Figure Object
    """
    # args[0] = 1 days
    # args[0][:1] = 1

    df = MeteoBlueDashboard(args[0][:1])
    
    df.generate_dash()

    return df.fig

