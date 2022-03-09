from django.contrib import admin

from UKCB.models import City, Review

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
     list_display = ('City','Rating', 'Price', 'Text')

class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('Name',)}

admin.site.register(City,CityAdmin)
admin.site.register(Review,ReviewAdmin)

