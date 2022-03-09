import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'UKCityBreaks.settings')

import django
import random
django.setup()
from UKCB.models import City, Review

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    London_Reviews = [
    {'Rating': 5,
    'Price':5,
     'text':'I Love London'},
    {'Rating': 5,
    'Price':5,
     'text':'I Really Love London'},
    {'Rating': 5,
    'Price':5,
     'text':'I Can Not Live without London'},]


    Glasgow_Reviews = [
    {'Rating': 5,
    'Price':5,
     'text':'I Love Glasgow'},
    {'Rating': 5,
    'Price':5,
     'text':'I Really Love Glasgow'},
    {'Rating': 5,
    'Price':5,
     'text':'I Can Not Live without Glasgow'},]

    Newcastle_upon_Tyne_Reviews = [
    {'Rating': 5,
    'Price':5,
     'text':'I Love Newcastle upon Tyne'},
    {'Rating': 5,
    'Price':5,
     'text':'I Really Love Newcastle upon Tyne'},
    {'Rating': 5,
    'Price':5,
     'text':'I Can Not Live without Newcastle upon Tyne'},]

    Cities = {'London': {'Reviews': London_Reviews,'Tag':'Example Tag','Description':'Example Description'},
    'Glasgow': {'Reviews': Glasgow_Reviews,'Tag':'Example Tag','Description':'Example Description'},
    'Newcastle upon Tyne': {'Reviews': Newcastle_upon_Tyne_Reviews,'Tag':'Example Tag','Description':'Example Description'} }


    # If you want to add more categories or pages,
    # add them to the dictionaries above.

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for city, city_data in Cities.items():
        c = add_city(city,city_data['Tag'],city_data['Description'])
        for r in city_data['Reviews']:
           add_review(c, r['Rating'], r['Price'],r['text'])

    # Print out the categories we have added.
    for c in City.objects.all():
        for r in Review.objects.filter(City=c):
            print(f'- {c}: {r}')

def add_review(city, rating, price, text):
    r = Review.objects.get_or_create(City=city, Text = text)[0]
    r.Rating = rating
    r.Price = price
    
    r.save()
    return r

def add_city(name, tag, description):
    c = City.objects.get_or_create(Name=name)[0]
    c.Tag = tag
    c.Description = description
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print('Starting UKCB population script...')
    populate()

