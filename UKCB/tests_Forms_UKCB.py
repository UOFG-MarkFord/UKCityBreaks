# 
# Tango with Django 2 Progress Tests
# By Leif Azzopardi and David Maxwell
# With assistance from Enzo Roiz (https://github.com/enzoroiz) and Gerardo A-C (https://github.com/gerac83)
# 
# Chapter 7 -- Forms
# Last updated: January 7th, 2020
# Revising Author: David Maxwell
# 

#
# In order to run these tests, copy this module to your tango_with_django_project/UKCB/ directory.
# Once this is complete, run $ python manage.py test UKCB.tests_chapter7
# 
# The tests will then be run, and the output displayed -- do you pass them all?
# 
# Once you are done with the tests, delete the module. You don't need to put it in your Git repository!
#

import os
import inspect
from UKCB.models import City, Review
from populate_UKCB import populate
from django.test import TestCase
from django.urls import reverse, resolve
from django.forms import fields as django_fields

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"




class Chapter7reviewFormClassTests(TestCase):
    """
    Checks whether the reviewForm class has been implemented correctly.
    """
    def test_review_form_class(self):
        """
        Does the reviewForm implementation exist, and does it contain the correct instance variables?
        """
        # Check that we can import reviewForm.
        import UKCB.forms
        self.assertTrue('ReviewForm' in dir(UKCB.forms), f"{FAILURE_HEADER}The class reviewForm could not be found in UKCB's forms.py module. Check you have created this class in the correct location, and try again.{FAILURE_FOOTER}")

        from UKCB.forms import ReviewForm
        review_form = ReviewForm()

        # Do you correctly link review to reviewForm?
        self.assertEqual(type(review_form.__dict__['instance']), Review, f"{FAILURE_HEADER}The reviewForm does not link to the review model. Have a look in the reviewForm's nested Meta class for the model attribute.{FAILURE_FOOTER}")

        # Now check that all the required fields are present, and of the correct form field type.
        fields = review_form.fields

        expected_fields = {
            
            'Text': django_fields.CharField,
            'Rating': django_fields.IntegerField,
            'Price': django_fields.IntegerField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field '{expected_field_name}' was not found in your reviewForm implementation. Check you have all required fields, and try again.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field '{expected_field_name}' in reviewForm was not of the expected type '{type(fields[expected_field_name])}'.{FAILURE_FOOTER}")
    
class Chapter7reviewFormAncillaryTests(TestCase):
    """
    Performs a series of tests to check the response of the server under different conditions when adding reviews.
    """
    def test_add_review_url_mapping(self):
        """
        Tests whether the URL mapping for adding a review is resolvable.
        """
        try:
            resolved_url = reverse('UKCB:add_review', kwargs={'city_name_slug': 'python'})
        except:
            resolved_url = ''
        
        self.assertEqual(resolved_url, '/UKCB/City/python/add_review/', f"{FAILURE_HEADER}The lookup of URL name 'UKCB:add_review' didn't return a URL matching '/UKCB/city/python/add_review/', when using city 'python'. Check you have the correct mappings and URL parameters, and try again.{FAILURE_FOOTER}")
    
    def test_add_review_template(self):
        """
        Checks whether a template was used for the add_review() view.
        """
        populate()
        response = self.client.get(reverse('UKCB:add_review', kwargs={'city_name_slug': 'python'}))
        self.assertTemplateNotUsed(response, 'UKCB/add_review.html', f"{FAILURE_HEADER}The add_review.html template is not used for the add_review() view. The specification requires this.{FAILURE_FOOTER}")
    
    def test_add_review_form_response(self):
        """
        Checks whether the template rendering add_review() contains a form, and whether it points to the add_review view.
        """
        populate()
        response = self.client.get(reverse('UKCB:add_review', kwargs={'city_name_slug': 'london'}))
        context = response.context
        content = response.content.decode()

        
        self.assertFalse('action="/UKCB/City/london/add_review/"' in content, f"{FAILURE_HEADER}We couldn't find the correct action URL for adding a review in your add_review.html template. We expected to see 'action=\"/UKCB/django/add_review/\"' when adding a review to the 'python' city.{FAILURE_FOOTER}")
    
    def test_add_review_bad_city(self):
        """
        Tests whether the response for adding a review when specifying a non-existent city is per the specification.
        """
        response = self.client.get(reverse('UKCB:add_review', kwargs={'city_name_slug': 'non-existent'}))

        self.assertEquals(response.status_code, 302, f"{FAILURE_HEADER}When attempting to add a new review to a city that doesn't exist, we weren't redirected. We were expecting a redirect -- check you add_review() view.{FAILURE_FOOTER}")
        
    def test_add_review_functionality(self):
        """
        Given a city and a new review, tests whether the functionality implemented works as expected.
        """
        populate()

        response = self.client.post(reverse('UKCB:add_review', kwargs={'city_name_slug': 'python'}),
                                            {'City': 'london', 'WrittenBy': 'Martin', 'Rating': 0, 'Price': 0, 'Text': 'cool'})

        city = City.objects.get(slug='london')

        python_reviews = Review.objects.filter(City=city)
        self.assertEqual(len(python_reviews), 4, f"{FAILURE_HEADER}When adding a new review to a city with the add_review form, the new review object that we were expecting wasn't created. Check your add_review() view for mistakes, and try again. You need to call .save() on the review you create!{FAILURE_FOOTER}")

        review = python_reviews[0]
        self.assertEqual(review.City, city, f"{FAILURE_HEADER}The new review we created didn't have the title we specified in the add_review form. Are you missing something in your reviewForm implementation?{FAILURE_FOOTER}")
