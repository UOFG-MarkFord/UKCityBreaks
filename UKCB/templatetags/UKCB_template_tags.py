from django import template
from UKCB.models import City

register = template.Library()

@register.inclusion_tag('UKCB/City.html')
def get_city_list(current_city=None):
    return {'cities': City.objects.all(),
            'current_city': current_city}

