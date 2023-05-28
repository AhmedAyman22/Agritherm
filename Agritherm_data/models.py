from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length = 25, primary_key = True)
    lat =  models.FloatField()
    lon =  models.FloatField()
    country = models.CharField(max_length = 25, default='')
    
    def __str__(self):
        return self.name