from django.urls import path
from . import views
# DO NOT DELETE THIS IMPORT, it's used by the dash library
from .Dash_Apps import meteorology_subplots, meteoblue_subplots, history_subplots


urlpatterns = [
    path('', views.dashboards, name='vaisala'),
    path('meteoblue/', views.meteoblue, name='meteoblue'),
    path('otherResources/', views.otherResources, name='otherResources'),
    path('webcams/', views.webcams, name='webcams'),
    path('history/', views.history, name='history'),
    path('allskycamera/', views.allskycamera, name='allskycamera'),
    path('nightlyskymovie/', views.nightlyskymovie, name='nightlyskymovie'),
    
]