from rest_framework import serializers
from .models import City


class citySerializer(serializers.ModelSerializers):
    class Meta:
        model = City
        fields = ('id', 'name', 'lat', 'lon')