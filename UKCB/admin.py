from django.contrib import admin

from UKCB.models import City, Review

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
     list_display = ('City','Rating', 'Price', 'Text')

admin.site.register(City)
admin.site.register(Review,ReviewAdmin)

