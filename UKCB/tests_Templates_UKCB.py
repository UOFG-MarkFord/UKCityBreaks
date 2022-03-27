# 
# Tango with Django 2 Progress Tests
# By Leif Azzopardi and David Maxwell
# With assistance from Gerardo A-C (https://github.com/gerac83) and Enzo Roiz (https://github.com/enzoroiz)
# 
# Chapter 8 -- Working with Templates
# Last updated: February 6th, 2020
# Revising Author: David Maxwell
# 

#
# In order to run these tests, copy this module to your tango_with_django_project/UKCB/ directory.
# Once this is complete, run $ python manage.py test UKCB.tests_chapter8
# 
# The tests will then be run, and the output displayed -- do you pass them all?
# 
# Once you are done with the tests, delete the module. You don't need to put it in your Git repository!
#

import os
import re
import inspect
from UKCB.models import City, Review
from populate_UKCB import populate
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.forms import fields as django_fields

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class Chapter8TemplateTests(TestCase):
    """
    I don't think it's possible to test every aspect of templates from this chapter without delving into some crazy string checking.
    So, instead, we can do some simple tests here: check that the base template exists, and that each Review in the templates/UKCB directory has a title block.
    Based on the idea by Gerardo -- beautiful idea, cheers big man.
    """
    def get_template(self, path_to_template):
        """
        Helper function to return the string representation of a template file.
        """
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()
        return template_str
    
    def test_base_template_exists(self):
        """
        Tests whether the base template exists.
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'UKCB', 'base.html')
        self.assertTrue(os.path.exists(template_base_path), f"{FAILURE_HEADER}We couldn't find the new base.html template that's required in the templates/UKCB directory. Did you create the template in the right place?{FAILURE_FOOTER}")
    
    def test_base_title_block(self):
        """
        Checks if UKCB's new base template has the correct value for the base template.
        """
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'UKCB', 'base.html')
        template_str = self.get_template(template_base_path)
        
        title_pattern = r'<title>(\s*|\n*)UKCB(\s*|\n*)-(\s*|\n*){% block title_block %}(\s*|\n*)UK City Breaks!(\s*|\n*){% (endblock|endblock title_block) %}(\s*|\n*)</title>'
        self.assertTrue(re.search(title_pattern, template_str), f"{FAILURE_HEADER}When searching the contents of base.html, we couldn't find the expected title block. We're looking for '<title>UKCB - {{% block title_block %}}How to Tango with Django!{{% endblock %}}</title>' with any combination of whitespace.{FAILURE_FOOTER}")
    
    

    def test_title_blocks(self):
        """
        Tests whether the title blocks in each Review are the expected values.
        This is probably the easiest way to check for blocks.
        """
        populate()
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'UKCB')
        
        mappings = {
            reverse('UKCB:AllCities'): {'full_title_pattern': r'<title>(\s*|\n*)UKCB(\s*|\n*)-(\s*|\n*)AllCities(\s*|\n*)</title>',
                                     'block_title_pattern': r'{% block title_block %}(\s*|\n*)AllCities(\s*|\n*){% (endblock|endblock title_block) %}',
                                     'template_filename': 'AllCities.html'},
           
          
            reverse('UKCB:index'): {'full_title_pattern': r'<title>(\s*|\n*)UKCB(\s*|\n*)-(\s*|\n*)Home(\s*|\n*)</title>',
                                     'block_title_pattern': r'{% block title_block %}(\s*|\n*)Home(\s*|\n*){% (endblock|endblock title_block) %}',
                                     'template_filename': 'index.html'},
        }

        for url in mappings.keys():
            full_title_pattern = mappings[url]['full_title_pattern']
            template_filename = mappings[url]['template_filename']
            block_title_pattern = mappings[url]['block_title_pattern']

            request = self.client.get(url)
            content = request.content.decode('utf-8')
            template_str = self.get_template(os.path.join(template_base_path, template_filename))

            self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}When looking at the response of GET '{url}', we couldn't find the correct <title> block. Check the exercises on Chapter 8 for the expected title.{FAILURE_FOOTER}")
            self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}When looking at the source of template '{template_filename}', we couldn't find the correct template block. Are you using template inheritence correctly, and did you spell the title as in the book? Check the exercises on Chapter 8 for the expected title.{FAILURE_FOOTER}")
    
    
