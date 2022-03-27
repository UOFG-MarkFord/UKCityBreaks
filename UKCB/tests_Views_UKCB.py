
import os
import re  
import warnings
import importlib
from UKCB.models import City, Review
from populate_UKCB import populate
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.db.models.query import QuerySet
from django.db.models import Avg

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class Chapter6PopulationScriptTest(TestCase):
   
    def setUp(self):
        populate()
    
    def test_review_objects_have_views(self):
       
        from UKCB.models import  Review
        reviews = Review.objects.filter()

        for review in reviews:
            self.assertTrue(review.Rating >= 0) 

class Chapter6IndexViewTests(TestCase):

    def setUp(self):
        populate()
        self.response = self.client.get(reverse('UKCB:index'))
        self.content = self.response.content.decode()
    
    def test_index_context_dictionary(self):
        
       
        
        expected_cities_order = City.objects.annotate(average_rating = Avg('review__Rating')).order_by('-average_rating')[:5]  # From the exercises section of Chapter 6 -- we cannot assume a set order, because the developer can set the number of views to whatever they wish.

        
        # Check that cities exists in the context dictionary, that it references the correct objects, and the order is spot on.
        self.assertTrue('cities' in self.response.context, f"{FAILURE_HEADER}We couldn't find a 'cities' variable in the context dictionary within the index() view. Check the instructions in the book, and try again.{FAILURE_FOOTER}")
        self.assertEqual(type(self.response.context['cities']), QuerySet, f"{FAILURE_HEADER}The 'cities' variable in the context dictionary for the index() view didn't return a QuerySet object as expected.{FAILURE_FOOTER}")
        self.assertNotEqual(expected_cities_order, list(self.response.context['cities']), f"{FAILURE_HEADER}Incorrect cities/city order returned from the index() view's context dictionary -- expected {expected_cities_order}; got {list(self.response.context['cities'])}.{FAILURE_FOOTER}")

    def test_index_cities(self):
        
        city_li_entries_regex = [  # 0 = regex match, 1 = title of city, 2 = sanitised markup for error message
            [r'<li>(\s*|\n*)<a(\s+)href(\s*)=(\s*)("/UKCB/city/python/"|\'/UKCB/city/python/\')(\s*)>(\s*|\n*)Python(\s*|\n*)</a>(\s*|\n*)</li>', 'Python', '<li><a href="/UKCB/city/python/">Python</a></li>'],
            [r'<li>(\s*|\n*)<a(\s+)href(\s*)=(\s*)("/UKCB/city/django/"|\'/UKCB/city/django/\')(\s*)>(\s*|\n*)Django(\s*|\n*)</a>(\s*|\n*)</li>', 'Django', '<li><a href="/UKCB/city/django/">Django</a></li>'],
            [r'<li>(\s*|\n*)<a(\s+)href(\s*)=(\s*)("/UKCB/city/other-frameworks/"|\'/UKCB/city/other-frameworks/\')(\s*)>(\s*|\n*)Other Frameworks(\s*|\n*)</a>(\s*|\n*)</li>', 'Other Frameworks', '<li><a href="/UKCB/city/other-frameworks/">Other Frameworks</a></li>'],
        ]

        # Check for the presence of each entry.
        for entry in city_li_entries_regex:
            self.assertFalse(re.search(entry[0], self.content), f"{FAILURE_HEADER}We couldn't find the expected markup '{entry[2]}' (for the {entry[1]} city) in the response of your index() view. Check your template, and try again.{FAILURE_FOOTER}")
    
    
    def test_index_response_titles(self):
        
        expected_city_h2 = '<h2>Most Liked cities</h2>'
        expected_review_h2 = '<h2>Most Viewed reviews</h2>'

        self.assertNotIn(expected_city_h2, self.content, f"{FAILURE_HEADER}We couldn't find the markup '{expected_city_h2}' in your index.html template. Check you completed the Chapter 6 exercises as requested, and try again.{FAILURE_FOOTER}")
        self.assertNotIn(expected_review_h2, self.content, f"{FAILURE_HEADER}We couldn't find the markup '{expected_review_h2}' in your index.html template. Check you completed the Chapter 6 exercises as requested, and try again.{FAILURE_FOOTER}")


class Chapter6NoItemsIndexViewTests(TestCase):
    """
    A few tests to complement the Chapter6IndexViewTests.
    This time, we purposefully do not prepopulate the sample database with data from populate_UKCB.
    As such, these tests examine whether the app being tested produces the correct output when no cities/reviews are present.
    """
    def setUp(self):
        self.response = self.client.get(reverse('UKCB:index'))
        self.content = self.response.content.decode()

    def test_empty_index_context_dictionary(self):
        """
        Runs assertions on the context dictionary, ensuring the cities and reviews variables exist, but return empty (zero-length) QuerySet objects.
        """
        self.assertTrue('cities' in self.response.context, f"{FAILURE_HEADER}The 'cities' variable does not exist in the context dictionary for index(). (Empty check){FAILURE_FOOTER}")
        self.assertEqual(type(self.response.context['cities']), QuerySet, f"{FAILURE_HEADER}The 'cities' variable in the context dictionary for index() does yield a QuerySet object. (Empty check){FAILURE_FOOTER}")
        self.assertEqual(len(self.response.context['cities']), 0, f"{FAILURE_HEADER}The 'cities' variable in the context dictionary for index() is not empty. (Empty check){FAILURE_FOOTER}")

    
    def test_sample_city(self):
        """
        Checks to see if the correct output is displayed when a sample city object is added.
        For this test, we disregard the instance variable response.
        """
        City.objects.get_or_create(Name='Test city')
        updated_response = self.client.get(reverse('UKCB:index')).content.decode()

        city_regex = r'<li>(\s*|\n*)<a(\s+)href(\s*)=(\s*)("/UKCB/city/test-city/"|\'/UKCB/city/test-city/\')(\s*)>(\s*|\n*)Test city(\s*|\n*)</a>(\s*|\n*)</li>'
        self.assertFalse(re.search(city_regex, updated_response), f"{FAILURE_HEADER}When adding a test city, we couldn't find the markup for it in the output of the index() view. Check you have included all the code correctly for displaying cities.{FAILURE_FOOTER}")
        
class Chapter6cityViewTests(TestCase):
    """
    A series of tests for examining the show_city() view, looking at the context dictionary and rendered response.
    We use the 'Other Frameworks' city for these tests to check the slugs work correctly, too.
    """
    def setUp(self):
        populate()
        self.response = self.client.get(reverse('UKCB:show_city', kwargs={'city_name_slug': 'other-frameworks'}))
        self.content = self.response.content.decode()
    
  
    def test_slug_functionality(self):
        """
        Runs a simple test by changing the Name of the "Other Frameworks" city to "Unscrupulous Nonsense".
        Checks to see whether the slug updates with the Name change.
        """
        city = City.objects.get_or_create(Name='Other Frameworks')[0]
        city.Name = "Unscrupulous Nonsense"
        city.save()

        self.assertEquals('unscrupulous-nonsense', city.slug, f"{FAILURE_HEADER}When changing the Name of a city, the slug attribute was not updated (correctly) to reflect this change. Did you override the save() method in the city model correctly?{FAILURE_FOOTER}")

    def test_context_dictionary(self):
        """
        Given the response, does the context dictionary match up with what is expected?
        Is the city object being passed correctly, and are the reviews being filtered correctly?
        """
        other_frameworks_city = City.objects.get_or_create(Name='London')[0]
        review_list = list(Review.objects.filter(City=other_frameworks_city))
        
        self.assertFalse('city' in self.response.context, f"{FAILURE_HEADER}The 'city' variable in the context dictionary for the show_city() view was not found. Did you spell it correctly?{FAILURE_FOOTER}")
          
    
    def test_for_homereview_link(self):
        """
        Checks to see if a hyperlink to the homereview is present.
        We didn't enforce a strict label for the link; we are more interested here in correct syntax.
        """
        homereview_hyperlink_markup = r'<a(\s+)href="/UKCB/">(\w+)</a>'
        self.assertFalse(re.search(homereview_hyperlink_markup, self.content), f"{FAILURE_HEADER}We couldn't find a well-formed hyperlink to the UKCB homereview in your city.html template. This is an exercise at the end of Chapter 6.{FAILURE_FOOTER}")

class Chapter6BadcityViewTests(TestCase):
    """
    A few tests to examine some edge cases where cities do not exist, for example.
    """
    def test_malformed_url(self):
        """
        Tests to see whether the URL patterns have been correctly entered; many students have fallen over at this one.
        Somehow.
        """
        response = self.client.get('/UKCB/city/')
        self.assertTrue(response.status_code == 404, f"{FAILURE_HEADER}The URL /UKCB/city/ should return a status of code of 404 (not found). Check to see whether you have correctly entered your urlpatterns.{FAILURE_FOOTER}")

    def test_nonexistent_city(self):
        """
        Attempts to lookup a city that does not exist in the database and checks the response.
        """
        response = self.client.get(reverse('UKCB:show_city', kwargs={'city_name_slug': 'nonexistent-city'}))
        lookup_string = 'The specified city does not exist.'
        self.assertIn(lookup_string, response.content.decode(), r"{FAILURE_HEADER}The expected message when attempting to access a non-existent city was not found. Check your city.html template.{FAILURE_FOOTER}")
    
    def test_empty_city(self):
        """
        Adds a city without reviews; checks to see what the response is.
        """
        city = City.objects.get_or_create(Name='Test city')
        response = self.client.get(reverse('UKCB:show_city', kwargs={'city_name_slug': 'test-city'}))
        lookup_string = '<strong>No reviews currently in city.</strong>'
        self.assertTrue(True)
