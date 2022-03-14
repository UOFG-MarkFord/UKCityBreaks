from django.urls import path
from UKCB import views
app_name = 'UKCB'

urlpatterns = [
    path('', views.index, name='index'),
    path('AllCities/', views.AllCities, name='AllCities'),
    path('City/<slug:city_name_slug>/',
        views.show_city, name='show_city'),
    path('City/<slug:city_name_slug>/add_review/', views.add_review, name='add_review'),
]

