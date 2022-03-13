from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from UKCB.models import City
from UKCB.models import Review
from UKCB.forms import CityForm, ReviewForm


# Create your views here.

def index(request):

    city_list = City.objects.order_by('-Name')[:5]
    
    context_dict = {}

    
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['cities'] = city_list
    
    return render(request, 'UKCB/index.html', context=context_dict)

def AllCities(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'This tutorial has been put together by WAD2 Team 14D '}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'UKCB/AllCities.html', context=context_dict)

   
def show_city(request, city_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        city = City.objects.get(slug=city_name_slug)
        
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        review = Review.objects.filter(City=city)
        
        # Adds our results list to the template context under name pages.
        context_dict['Reviews'] = review
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['City'] = city
    except City.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['City'] = None
        context_dict['Reviews'] = None
        
    # Go render the response and return it to the client.
    return render(request, 'UKCB/City.html', context=context_dict)

def add_city(request):

    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            return redirect('/UKCB/')
        else:
            print(form.errors)

    return render(request, 'UKCB/add_city.html', {'form': form})

def add_review(request, city_name_slug):
    try:
        city = City.objects.get(slug=city_name_slug)
    except:
        city = None
    
    if city is None:
        return redirect('/UKCB/')

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            if city:
                review = form.save(commit=False)
                review.city = city
                review.rating = 0
                review.price = 0
                review.save()
                return redirect(reverse('UKCB:show_city',
                                        kwargs={'city_name_slug': city_name_slug}))
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'city': city}
    return render(request, 'UKCB/add_review.html', context=context_dict)