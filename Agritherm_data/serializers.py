from rest_framework import serializers
from .models import *


class citySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'lat', 'lon', 'country')
        
class promptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ('id', 'prompt')
        
        
class responseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('id', 'response', 'user')