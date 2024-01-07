from django.urls import path
from . import views
from .Dash_Apps import meteorology_subplots, meteoblue_subplots


urlpatterns = [
    path('', views.dashboards, name='vaisala'),
    path('meteoblue/', views.meteoblue, name='meteoblue'),
]