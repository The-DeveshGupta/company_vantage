from django.contrib import admin
from django.urls import path
from . import views

app_name = 'data_predictor'

urlpatterns = [
    path('healthcheck/', views.healthcheck),
]
