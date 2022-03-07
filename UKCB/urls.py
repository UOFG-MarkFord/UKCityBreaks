from django.urls import path
from UKCB import views
app_name = 'UKCB'

urlpatterns = [
    path('', views.index, name='index'),
    path('AllCities/', views.AllCities, name='AllCities'),
]

