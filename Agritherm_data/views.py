from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *

# Create your views here.


class cityView(APIView):
    def get(self, request):
        allCities = City.objects.all().values()
        return Response({allCities})
    
    def post(self, request):
        City.objects.create(
                            id= request.data["id"],
                            name= request.data["name"],
                            lat= request.data["lat"],
                            lon= request.data["lon"]
                            )
        
        city = City.object.all().filter(id=request.data["id"]).values()
        return Response({"Message":"City Entry", "City:":city})