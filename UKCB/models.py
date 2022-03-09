from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class City(models.Model):

    CityID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=64)
    Tag =  models.CharField(max_length=64)
    Description = models.CharField(max_length=2048)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.Name)
        super(City, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Cities'

        
    def __str__(self):
        return self.Name
    
class Review(models.Model):

    
    ReviewID = models.AutoField(primary_key=True)
    
    City = models.ForeignKey(City, on_delete=models.CASCADE)
    
    Rating = models.IntegerField(default=0)
    
    Price = models.IntegerField(default=0)
    
    Text = models.CharField(max_length=2048)

    
    def __str__(self):
        return self.Text
