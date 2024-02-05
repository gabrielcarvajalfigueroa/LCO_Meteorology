from django.shortcuts import render
from lcodataclient import dataclient
import pandas as pd
import plotly.graph_objects as go 
from plotly.offline import plot
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
# DO NOT delete this import, it's used by the dash library
from .Dash_Apps import meteorology_subplots, meteoblue_subplots, history_subplots


# Create your views here.
def dashboards(request):

    template = loader.get_template("index.html")

    now = datetime.now()

    now_string = "Forecast update: " + now.strftime("%Y-%m-%d %H:%M")

    context = {
        'data' : now_string
    } 
    

    return HttpResponse(template.render(context, request))

def meteoblue(request):

    template = loader.get_template("meteoblue.html")
    
    now = datetime.now()

    now_string = "Forecast update: " + now.strftime("%Y-%m-%d %H:%M") + " (UTC)"

    context = {
        'data' : now_string
    } 

    return HttpResponse(template.render(context, request))  

def otherResources(request):

    template = loader.get_template("otherResources.html")
    
    now = datetime.now()

    now_string = "Forecast update: " + now.strftime("%Y-%m-%d %H:%M")

    context = {
        'data' : now_string
    } 

    return HttpResponse(template.render(context, request))      

def webcams(request):

    template = loader.get_template("webcams.html")
    
    now = datetime.now()

    now_string = "Forecast update: " + now.strftime("%Y-%m-%d %H:%M")

    context = {
        'data' : now_string
    } 

    return HttpResponse(template.render(context, request))    

def history(request):

    template = loader.get_template("history.html")

    context = {
        'data' : ''
    } 

    return HttpResponse(template.render(context, request)) 

def allskycamera(request):

    template = loader.get_template("allskycamera.html")

    context = {
        'data' : ''
    } 

    return HttpResponse(template.render(context, request))     