from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
# DO NOT DELETE THIS IMPORT, it's used by the dash library
from .Dash_Apps import meteorology_subplots, meteoblue_subplots, history_subplots


# ----------------- View for Vaisala Dashboard ------------------------ #
def dashboards(request):

    template = loader.get_template("index.html")    

    context = {'data' : ''}
    
    return HttpResponse(template.render(context, request))

# ----------------- View for Meteoblue Dashboard ------------------------ #

def meteoblue(request):

    template = loader.get_template("meteoblue.html")
    
    now = datetime.now()

    now_string = "Forecast update: " + now.strftime("%Y-%m-%d %H:%M") + " (UTC)"

    context = {
        'data' : now_string
    } 

    return HttpResponse(template.render(context, request))  

# ----------------- View for otherResources ------------------------ #

def otherResources(request):

    template = loader.get_template("otherResources.html")
    
    context = {'data' : ''}

    return HttpResponse(template.render(context, request))      

# ----------------- View for Red/Blue Webcams ------------------------ #

def webcams(request):

    template = loader.get_template("webcams.html")
    
    context = {'data' : ''}

    return HttpResponse(template.render(context, request))    

# ----------------- View for History Dashboard ------------------------ #

def history(request):

    template = loader.get_template("history.html")

    context = {'data' : ''} 

    return HttpResponse(template.render(context, request)) 

# ----------------- View for Allsky Camera ------------------------ #

def allskycamera(request):

    template = loader.get_template("allskycamera.html")

    context = {'data' : ''}

    return HttpResponse(template.render(context, request))     

# ----------------- View for Nightsky movie video ------------------------ #

def nightlyskymovie(request):

    template = loader.get_template("nightlyskymovie.html")

    context = {'data' : ''} 

    return HttpResponse(template.render(context, request))