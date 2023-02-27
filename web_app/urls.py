from django.contrib import admin
from django.urls import path
from . import views

app_name = 'web_app'

urlpatterns = [
    path('healthcheck/', views.healthcheck),
    path('', views.index, name='home'),
    path('company/', views.company, name='company'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
]
