from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("<a href='/UKCB/about/'>About</a> Rango says hey there partner!")

def about(request):
    return HttpResponse(" <a href='/UKCB/'>Index</a>Rango says here is the about page.")
