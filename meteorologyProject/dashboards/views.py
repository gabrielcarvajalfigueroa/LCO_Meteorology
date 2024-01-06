from django.shortcuts import render
from lcodataclient import dataclient
import pandas as pd
import plotly.graph_objects as go 
from plotly.offline import plot
from django.http import HttpResponse
from django.template import loader
from .plotly_graphs import *
from .Dash_Apps import meteorology_subplots, meteoblue_subplots

# Create your views here.
def dashboards(request):

    template = loader.get_template("index.html")

    #target_plot = plotly_plot('temperature')
    #target_plot_wind = plotly_plot_wind()

    context = {
        'data' : "hola"#target_plot_wind
    } 
    

    return HttpResponse(template.render(context, request))

