from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from datetime import datetime
# DO NOT DELETE THIS IMPORT, it's used by the dash library
from .Dash_Apps import meteorology_subplots, meteoblue_subplots, history_subplots


import environ

env= environ.Env()
environ.Env.read_env()

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
    
    context = {'northwebcam_png': env('NORTHWEBCAM_PNG'),
               'northwebcam_gif': env('NORTHWEBCAM_GIF'),
               'westwebcam_png': env('WESTWEBCAM_PNG'),
               'westwebcam_gif': env('WESTWEBCAM_GIF'),
               'southwebcam_png': env('SOUTHWEBCAM_PNG'),
               'southwebcam_gif': env('SOUTHWEBCAM_GIF')}

    return HttpResponse(template.render(context, request))    

# ----------------- View for History Dashboard ------------------------ #

def history(request):

    template = loader.get_template("history.html")

    context = {'data' : ''} 

    return HttpResponse(template.render(context, request)) 

# ----------------- View for Allsky Camera ------------------------ #

def allskycamera(request):

    template = loader.get_template("allskycamera.html")

    context = {'bluefilter_png': env('BLUEFILTER_PNG'),
               'bluefilter_gif': env('BLUEFILTER_GIF'),
               'redfilter_png': env('REDFILTER_PNG'),
               'redfilter_gif': env('REDFILTER_GIF')}

    return HttpResponse(template.render(context, request))     

# ----------------- View for Nightsky movie video ------------------------ #

def nightlyskymovie(request):

    template = loader.get_template("nightlyskymovie.html")

    context = {'nightlyskymovie' : env('NIGHTLYSKYMOVIE')} 

    return HttpResponse(template.render(context, request))