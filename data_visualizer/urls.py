from django.contrib import admin
from django.urls import path
from . import views

app_name = 'data_visualizer'

urlpatterns = [
    path('healthcheck/', views.healthcheck),
]