import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'UKCityBreaks.settings')

import django
import random
django.setup()
from UKCB.models import City, Review, UserProfile
from django.contrib.auth.models import User
import re


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    decription = []
    tag = []

    with open('description.txt') as f:
       for line in f:
          
           decription.append( re.sub(r'[^A-Za-z0-9 ]+', '', line))

    with open('tag.txt') as f:
       for line in f:
          
           tag.append( re.sub(r'[^A-Za-z0-9 ]+', '', line))
       


    London_Reviews = [
    {'Rating': 5,
    'Price':5,
     'text':'I Love London'},
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
     'text':'I Love Glasgow'},
    {'Rating': 5,
    'Price':5,
     'text':'I Love Glasgow'},
    {'Rating': 5,
    'Price':5,
     'text':'I Really Love Glasgow'},
    {'Rating': 3,
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

    Newport_Reviews = [
    {'Rating': 5,
    'Price':5,
     'text':'I Love Newport'},
    {'Rating': 5,
    'Price':5,
     'text':'I Really Love Newport'},
    {'Rating': 5,
    'Price':5,
     'text':'I Can Not Live without Newport'},]

    Newry_Reviews = [
    {'Rating': 5,
    'Price':5,
     'text':'I Love Newry'},
    {'Rating': 5,
    'Price':5,
     'text':'I Really Love Newry'},
    {'Rating': 5,
    'Price':5,
     'text':'I Can Not Live without Newry'},]

    Edinburgh_Reviews = [
    {'Rating': 0,'Price':5,'text':'I Hate Edinburgh'},
    {'Rating': 0,'Price':5,'text':'I Really Hate Edinburgh'},
    {'Rating': 0,'Price':5,'text':'I Can Not Live without Hating Edinburgh'},]

    Oxford_Reviews = [
    {'Rating': 0,'Price':5,'text':'I Hate Oxford'},
    {'Rating': 0,'Price':5,'text':'I Really Hate Oxford'},
    {'Rating': 0,'Price':5,'text':'I Can Not Live without Hating Oxford'},]
     
    Cambridge_Reviews = [
    {'Rating': 0,'Price':5,'text':'I Hate Cambridge'},
    {'Rating': 0,'Price':5,'text':'I Really Hate Cambridge'},
    {'Rating': 0,'Price':5,'text':'I Can Not Live without Hating Cambridge'},]

    Manchester_Reviews = [
    {'Rating': 3,'Price':3,'text':'I like Manchester'},
    {'Rating': 3,'Price':3,'text':'I Really am ok with Manchester'},
    {'Rating': 3,'Price':3,'text':'I Could honestly Live without Manchester'},]
    
    Liverpool_Reviews = [
    {'Rating': 3,'Price':3,'text':'I like Liverpool'},
    {'Rating': 3,'Price':3,'text':'I Really am ok with Liverpool'},
    {'Rating': 3,'Price':3,'text':'I Could honestly Live without Liverpool'},]

    Birmingham_Reviews = [
    {'Rating': 3,'Price':3,'text':'I like Birmingham'},
    {'Rating': 3,'Price':3,'text':'I Really am ok with Birmingham'},
    {'Rating': 3,'Price':3,'text':'I Could honestly Live without Birmingham'},]

    Bristol_Reviews = [
    {'Rating': 3,'Price':3,'text':'I like Bristol'},
    {'Rating': 3,'Price':3,'text':'I Really am ok with Bristol'},
    {'Rating': 3,'Price':3,'text':'I Could honestly Live without Bristol'},]

    Brighton_Reviews = [
    {'Rating': 3,'Price':3,'text':'I like Brighton'},
    {'Rating': 3,'Price':3,'text':'I Really am ok with Brighton'},
    {'Rating': 3,'Price':3,'text':'I Could honestly Live without Brighton'},]

    Aberdeen_Reviews = [
    {'Rating': 5,'Price':0,'text':'I like Aberdeen'},
    {'Rating': 3,'Price':0,'text':'I Really am ok with Aberdeen'},
    {'Rating': 5,'Price':0,'text':'I Could honestly Live without Aberdeen'},
    {'Rating': 3,'Price':0,'text':'I Could honestly Live without Aberdeen'},
    {'Rating': 5,'Price':0,'text':'I Could honestly Live without Aberdeen'},]

    Stirling_Reviews = [
    {'Rating': 5,'Price':0,'text':'I like Stirling'},
    {'Rating': 5,'Price':0,'text':'I Really am ok with Stirling'},
    {'Rating': 5,'Price':0,'text':'I Could honestly Live without Stirling'},]

    Dundee_Reviews = [
    {'Rating': 0,'Price':0,'text':'Risked my life going here'},]

    Perth_Reviews = [
    {'Rating': 0,'Price':0,'text':'Risked my life going here'},]

    Inverness_Reviews = [
    {'Rating': 0,'Price':0,'text':'Loch Ness Monster is not real :('},]


    Cities = {'London': {'Reviews': London_Reviews,'Tag':tag[0],'Description':decription[0]},
    'Glasgow': {'Reviews': Glasgow_Reviews,'Tag':tag[1],'Description':decription[1]},
    'Newcastle upon Tyne': {'Reviews': Newcastle_upon_Tyne_Reviews,'Tag':tag[2],'Description':decription[2]},
    'Newport': {'Reviews': Newport_Reviews,'Tag':tag[3],'Description':decription[3]},
    'Newry': {'Reviews': Newry_Reviews,'Tag':tag[4],'Description':decription[4]},
    'Edinburgh': {'Reviews': Edinburgh_Reviews,'Tag':tag[5],'Description':decription[5]},
    'Oxford': {'Reviews': Oxford_Reviews,'Tag':tag[6],'Description':decription[6]},
    'Cambridge': {'Reviews': Cambridge_Reviews,'Tag':tag[7],'Description':decription[7]},
    'Manchester': {'Reviews': Manchester_Reviews,'Tag':tag[8],'Description':decription[8]},
    'Liverpool': {'Reviews': Liverpool_Reviews,'Tag':tag[9],'Description':decription[9]},
    'Birmingham': {'Reviews': Birmingham_Reviews,'Tag':tag[10],'Description':decription[10]},
    'Bristol': {'Reviews': Bristol_Reviews,'Tag':tag[11],'Description':decription[11]},
    'Brighton': {'Reviews': Brighton_Reviews,'Tag':tag[12],'Description':decription[12]},
    'Aberdeen': {'Reviews': Aberdeen_Reviews,'Tag':tag[13],'Description':decription[13]},
    'Stirling': {'Reviews': Stirling_Reviews,'Tag':tag[14],'Description':decription[14]},
    'Dundee': {'Reviews': Dundee_Reviews,'Tag':tag[15],'Description':decription[15]},
    'Perth': {'Reviews': Perth_Reviews,'Tag':tag[16],'Description':decription[16]},
    'Inverness': {'Reviews': Inverness_Reviews,'Tag':tag[17],'Description':decription[17]},

    }

    Users = [{'name':'Mary','password':'password'},{'name':'Martin','password':'password'},{'name':'Marvin','password':'password'},
             {'name':'Aleksy','password':'password'},{'name':'Martina','password':'password'}]
    
    # If you want to add more categories or pages,
    # add them to the dictionaries above.


    
    for u in Users:
        add_user(u['name'], u['password'])

    
    
    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    
    for city, city_data in Cities.items():
        
        c = add_city(city,city_data['Tag'],city_data['Description'])
        counter = 0
        
        for r in city_data['Reviews']:

            if counter >= len(Users):
                counter = 0
                
            user = Users[counter]['name']

            counter += 1
            
            add_review(c, r['Rating'], r['Price'],r['text'],User.objects.get(username=user))
           

           


def add_review(city, rating, price, text, writtenBy):
    r = Review.objects.get_or_create(City=city, WrittenBy = writtenBy)[0]
    r.Text = text
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

def add_user(name, password):
    
    if not User.objects.filter(username=name).exists():

        User.objects.create_user(name,password = password)
        
    
    return None

# Start execution here!
if __name__ == '__main__':
    print('Starting UKCB population script...')
    populate()

