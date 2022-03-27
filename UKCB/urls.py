from django.urls import path

from django.contrib.auth import views as auth_views
from UKCB import views


app_name = 'UKCB'

urlpatterns = [
    path('', views.index, name='index'),
    path('AllCities/', views.AllCities, name='AllCities'),

    path('City/<slug:city_name_slug>/',
        views.show_city, name='show_city'),
    path('City/<slug:city_name_slug>/add_review/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('MyAccount/', views.MyAccount, name='MyAccount'),
]


