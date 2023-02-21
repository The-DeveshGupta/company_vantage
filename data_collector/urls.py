from django.contrib import admin
from django.urls import path
from . import views

app_name = 'data_collector'

urlpatterns = [
    path('healthcheck/', views.healthcheck),
    path('stocks_data/', views.stocks_data)
]