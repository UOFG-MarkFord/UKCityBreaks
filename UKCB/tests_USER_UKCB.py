# 
# Tango with Django 2 Progress Tests
# By Leif Azzopardi and David Maxwell
# With assistance from Gerardo A-C (https://github.com/gerac83) and Enzo Roiz (https://github.com/enzoroiz)
# 
# Chapter 9 -- Forms
# Last updated: February 6th, 2020
# Revising Author: David Maxwell
# 

#
# In order to run these tests, copy this module to your tango_with_django_project/UKCB/ directory.
# Once this is complete, run $ python manage.py test UKCB.tests_chapter9
# 
# The tests will then be run, and the output displayed -- do you pass them all?
# 
# Once you are done with the tests, delete the module. You don't need to put it in your Git repository!
#

import os
import re
import inspect
import tempfile
import UKCB.models
from UKCB import forms
from populate_UKCB import populate
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"


def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user

def create_super_user_object():
    """
    Helper function to create a super user (admin) account.
    """
    return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

def get_template(path_to_template):
    """
    Helper function to return the string representation of a template file.
    """
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str

class Chapter9SetupTests(TestCase):
    """
    A simple test to check whether the auth app has been specified.
    """
    def test_installed_apps(self):
        """
        Checks whether the 'django.contrib.auth' app has been included in INSTALLED_APPS.
        """
        self.assertTrue('django.contrib.auth' in settings.INSTALLED_APPS)


class Chapter9ModelTests(TestCase):
    """
    Tests to check whether the UserProfile model has been created according to the specification.
    """
    def test_userprofile_class(self):
        """
        Does the UserProfile class exist in UKCB.models? If so, are all the required attributes present?
        Assertion fails if we can't assign values to all the fields required (i.e. one or more missing).
        """
        self.assertTrue('UserProfile' in dir(UKCB.models))

        user_profile = UKCB.models.UserProfile()

        # Now check that all the required attributes are present.
        # We do this by building up a UserProfile instance, and saving it.
        expected_attributes = {
           
            'user': create_user_object(),
        }

        expected_types = {
          
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile model.{FAILURE_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])
        
        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}. Check your implementation and try again.{FAILURE_FOOTER}")
        user_profile.save()
    



class Chapter9LoginTests(TestCase):
    """
    A series of tests for checking the login functionality of UKCB.
    """
    def test_login_url_exists(self):
        """
        Checks to see if the new login view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('UKCB:login')
        except:
            pass
        
        self.assertEqual(url, '/UKCB/login/', f"{FAILURE_HEADER}Have you created the UKCB:login URL mapping correctly? It should point to the new login() view, and have a URL of '/UKCB/login/' Remember the first part of the URL (/UKCB/) is handled by the project's urls.py module, and the second part (login/) is handled by the UKCB app's urls.py module.{FAILURE_FOOTER}")

    def test_login_functionality(self):
        """
        Tests the login functionality. A user should be able to log in, and should be redirected to the UKCB homereview.
        """
        user_object = create_user_object()

        response = self.client.post(reverse('UKCB:login'), {'username': 'testuser', 'password': 'testabc123'})
        
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in with your login() view, it didn't seem to log the user in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Testing your login functionality, logging in was successful. However, we expected a redirect; we got a status code of {response.status_code} instead. Check your login() view implementation.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('UKCB:index'), f"{FAILURE_HEADER}We were not redirected to the UKCB homereview after logging in. Please check your login() view implementation, and try again.{FAILURE_FOOTER}")

    def test_login_template(self):
        """
        Does the login.html template exist in the correct place, and does it make use of template inheritance?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'UKCB')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'login.html' template in the 'templates/UKCB/' directory. Did you put it in the right place?{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        full_title_pattern = r'<title>(\s*|\n*)UKCB(\s*|\n*)-(\s*|\n*)Login(\s*|\n*)</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Login(\s*|\n*){% (endblock|endblock title_block) %}'

        request = self.client.get(reverse('UKCB:login'))
        content = request.content.decode('utf-8')

        self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}The <title> of the response for 'UKCB:login' is not correct. Check your login.html template, and try again.{FAILURE_FOOTER}")
        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}Is login.html using template inheritance? Is your <title> block correct?{FAILURE_FOOTER}")
    
    def test_login_template_content(self):
        """
        Some simple checks for the login.html template. Is the required text present?
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'UKCB')
        template_path = os.path.join(template_base_path, 'login.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'login.html' template in the 'templates/UKCB/' directory. Did you put it in the right place?{FAILURE_FOOTER}")
        
        template_str = get_template(template_path)
        self.assertTrue('<h1>Login to UKCityBreaks</h1>' in template_str, f"{FAILURE_HEADER}We couldn't find the '<h1>Login to UKCB</h1>' in the login.html template.{FAILURE_FOOTER}")
        self.assertTrue('action="{% url \'UKCB:login\' %}"' in template_str, f"{FAILURE_HEADER}We couldn't find the url lookup for 'UKCB:login' in your login.html <form>.{FAILURE_FOOTER}")

    
class Chapter9LogoutTests(TestCase):
    """
    A few tests to check the functionality of logging out. Does it work? Does it actually log you out?
    """
    def test_bad_request(self):
        """
        Attepts to log out a user who is not logged in.
        This should according to the book redirect you to the login review.
        """
        response = self.client.get(reverse('UKCB:logout'))
        self.assertTrue(response.status_code, 302)
        self.assertTrue(response.url, reverse('UKCB:login'))
    
    def test_good_request(self):
        """
        Attempts to log out a user who IS logged in.
        This should succeed -- we should be able to login, check that they are logged in, logout, and perform the same check.
        """
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}We attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. Please check your login() view. This happened when testing logout functionality.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log a user in, it failed. Please check your login() view and try again.{FAILURE_FOOTER}")
        
        # Now lot the user out. This should cause a redirect to the homereview.
        response = self.client.get(reverse('UKCB:logout'))
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Logging out a user should cause a redirect, but this failed to happen. Please check your logout() view.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('UKCB:index'), f"{FAILURE_HEADER}When logging out a user, the book states you should then redirect them to the homereview. This did not happen; please check your logout() view.{FAILURE_FOOTER}")
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}Logging out with your logout() view didn't actually log the user out! Please check yout logout() view.{FAILURE_FOOTER}")


class Chapter9LinkTidyingTests(TestCase):
    """
    Some checks to see whether the links in base.html have been tidied up and change depending on whether a user is logged in or not.
    We don't check for city/review links here; these are done in the exercises.
    """
    def test_omnipresent_links(self):
        """
        Checks for links that should always be present, regardless of user state.
        """
        content = self.client.get(reverse('UKCB:index')).content.decode()
        self.assertTrue('href="/UKCB/"' in content)

        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')

        # These should be present.
        content = self.client.get(reverse('UKCB:index')).content.decode()
        self.assertTrue('href="/UKCB/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
    
    def test_logged_in_links(self):
        """
        Checks for links that should only be displayed when the user is logged in.
        """
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        content = self.client.get(reverse('UKCB:index')).content.decode()

        # These should be present.
        
        self.assertTrue('href="/UKCB/logout/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")

        # These should not be present.
        self.assertTrue('href="/UKCB/login/"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        self.assertTrue('href="/UKCB/register/"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
    
    def test_logged_out_links(self):
        """
        Checks for links that should only be displayed when the user is not logged in.
        """
        content = self.client.get(reverse('UKCB:index')).content.decode()

        # These should be present.
        self.assertTrue('href="/UKCB/login/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        self.assertTrue('href="/UKCB/register/"' in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")
        
        # These should not be present.
        
        self.assertTrue('href="/UKCB/logout/"' not in content, f"{FAILURE_HEADER}Please check the links in your base.html have been updated correctly to change when users log in and out.{FAILURE_FOOTER}")


class Chapter9ExerciseTests(TestCase):
    """
    A series of tests to check whether the exercises in Chapter 9 have been implemented correctly.
    We check that there is a restricted.html template, whether it uses inheritance, and checks that adding cateories and reviews can only be done by a user who is logged in.
    """
   
    def test_bad_add_review(self):
        """
        Tests to see if a review cannot be added when not logged in.
        """
        populate()
        response = self.client.get(reverse('UKCB:add_review', kwargs={'city_name_slug': 'python'}))

        
        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}When not logged in and attempting to add a review, we should be redirected. But we weren't. Check your add_review() implementation.{FAILURE_FOOTER}")
        self.assertTrue(response.url.startswith(reverse('UKCB:login')), f"{FAILURE_HEADER}When not logged in and attempting to add a review, we should be redirected to the login review. But we weren't. Check your add_review() implementation.{FAILURE_FOOTER}")
    
    def test_good_add_review(self):
        """
        Tests to see if a review can be added when logged in.
        """
        populate()
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        response = self.client.get(reverse('UKCB:add_review', kwargs={'city_name_slug': 'python'}))

        
        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}We weren't greeted with a HTTP status code when attempting to add a review when logged in. Check your add_review() view.{FAILURE_FOOTER}")
        
    
    def test_add_review_link(self):
        """
        Tests to see if the Add review link only appears when logged in.
        """
        populate()
        content = self.client.get(reverse('UKCB:show_city', kwargs={'city_name_slug': 'python'})).content.decode()
        
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        content = self.client.get(reverse('UKCB:show_city', kwargs={'city_name_slug': 'python'})).content.decode()


