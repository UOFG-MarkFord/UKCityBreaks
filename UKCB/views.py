from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from UKCB.models import City
from UKCB.models import Review
from UKCB.forms import ReviewForm
from django.shortcuts import redirect
from django.urls import reverse
from UKCB.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from django.db import models
from django.db.models import Avg

# Create your views here.

def index(request):

    if 'term' in request.GET:
        qs = City.objects.filter(Name__istartswith = request.GET.get('term'))
        names =  list()
        for name in qs:
            names.append(name.Name)
        return JsonResponse(names, safe = False)
    
    
    city_list = City.objects.annotate(average_rating = Avg('review__Rating')).order_by('-average_rating')[:5]
    most_popular = City.objects.annotate(num_reviews=Count('review')).order_by('-num_reviews')[:5]
    
    context_dict = {}
    
    context_dict['cities'] = list(city_list)
    context_dict['popCities'] = most_popular
    
    return render(request, 'UKCB/index.html', context=context_dict)

def AllCities(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'This tutorial has been put together by WAD2 Team 14D '}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'UKCB/AllCities.html', context=context_dict)

   
def show_city(request, city_name_slug ):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    
    context_dict = {}
   
    searched = request.POST.get('searched', False)
    
    if searched:
        city_name_slug = searched.replace(' ','-').lower()
    
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



@login_required
def add_review(request, city_name_slug):

    try:
        city = City.objects.get(slug=city_name_slug)
    except City.DoesNotExist:
        city = None

    current_user = request.user
    
    # You cannot add a page to a Category that does not exist...
    if city is None:
        return redirect('/UKCB/')
    
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        
        if form.is_valid():
           if city:
                review = form.save(commit=False)
                review.City = city
                review.WrittenBy = current_user
                
                review.save()
                return redirect(reverse('UKCB:show_city', kwargs={'city_name_slug':city_name_slug}))
            
        else:
            print(form.errors)
            
    context_dict = {'form': form, 'city': city}
    return render(request, 'UKCB/add_review.html', context=context_dict)

def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model

            # until we're ready to avoid integrity problems.
           

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        

    # Render the template depending on the context.
    return render(request,
        'UKCB/register.html',
        context = {'user_form': user_form,
                'registered': registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('UKCB:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your UKCityBreaks account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
            # The request is not a HTTP POST, so display the login form.

            # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'UKCB/login.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('UKCB:index'))

@login_required
def MyAccount(request):
    
    context_dict = {}
    
    current_user = request.user
    
    review = Review.objects.filter(WrittenBy=current_user)
        
    # Adds our results list to the template context under name pages.
    context_dict['Reviews'] = review
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict['boldmessage'] = 'This tutorial has been put together by Cool Dudes '
    
    
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'UKCB/MyAccount.html', context=context_dict)
