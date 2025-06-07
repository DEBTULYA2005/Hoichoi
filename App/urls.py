from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('About', views.about, name='About'),
    path('login', views.login, name='login'),
    path('otp_verify', views.otp_verify, name='otp_verify'),
]
