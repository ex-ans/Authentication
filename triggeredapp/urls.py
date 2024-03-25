from django.contrib import admin
from django.urls import path
from triggeredapp import views

urlpatterns = [
    path('' , views.index , name='index'), 
    path('home' , views.home , name='home'),
    path('verification' , views.verification , name='verification'),
    path('signin' , views.signin , name='signin'), 
    path('signup' , views.signup , name='signup'),
    path('logoutUser' , views.logoutUser , name='logoutUser'),

   
]
