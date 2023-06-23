import os
import json
import django
import sys
# Set up Django environment
path = 'Z:\Agritherm\Agritherm'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Agritherm.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agritherm.settings')
django.setup()

from Agritherm_data.models import City

def import_cities():
    with open('cities.json') as json_file:
        json_file = json.load(json_file)
        json_file['names']
        countries = [None] * 18
        for i in range(len(json_file['names'])):
            countries[i] = json_file['names'][i]
            print(countries[i])
        for i in range(len(countries)):
            country = countries[i]
            name = json_file[countries[i]]['city_1']
            lat = json_file[countries[i]]['latitude1']
            lon = json_file[countries[i]]['longitude1']
            print(name, country)
            city = City(name=name, lat=lat, lon=lon, country = country)
            city.save()
            name = json_file[countries[i]]['city_2']
            lat = json_file[countries[i]]['latitude2']
            lon = json_file[countries[i]]['longitude2']
            print(name, country)
            city = City(name=name, lat=lat, lon=lon, country = country)
            city.save()
            name = json_file[countries[i]]['city_3']
            lat = json_file[countries[i]]['latitude3']
            lon = json_file[countries[i]]['longitude3']
            print(name, country)
            city = City(name=name, lat=lat, lon=lon, country = country)
            city.save()
if __name__ == '__main__':
    import_cities()
