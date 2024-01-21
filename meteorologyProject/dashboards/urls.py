from django.urls import path
from . import views
# DO NOT delete this import, it's used by the dash library
from .Dash_Apps import meteorology_subplots, meteoblue_subplots



urlpatterns = [
    path('', views.dashboards, name='vaisala'),
    path('meteoblue/', views.meteoblue, name='meteoblue'),
    path('otherResources/', views.otherResources, name='otherResources'),
    
]