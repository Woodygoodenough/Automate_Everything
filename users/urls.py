"""Defining urls for registration"""
from django.urls import path, include
from . import views

app_name = 'users'  #  This variable is important for Django to recognize a correct url pattern
urlpatterns = [
    #  Include default auth urls. containing pages '/login' and '/logout' with name of 'login' and 'logout'.
    #  When make a request to these pages, Django's default view file handles the request and looks for login/logout
    #  template under the registration directory
    path('', include('django.contrib.auth.urls')),
    # Registration page.
    path('register/', views.register, name='register'),
]