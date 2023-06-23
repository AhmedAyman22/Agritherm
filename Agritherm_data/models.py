from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length = 25, primary_key = True)
    lat =  models.FloatField()
    lon =  models.FloatField()
    country = models.CharField(max_length = 25, default='')
    
    def __str__(self):
        return self.name
    
class Prompt(models.Model):
    prompt = models.CharField(max_length = 60, null=True)
    
class Response(models.Model):
    response = models.CharField(max_length = 70)
    user = models.ForeignKey(Prompt, blank=True, null=True,on_delete=models.CASCADE)