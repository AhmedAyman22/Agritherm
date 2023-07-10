import json
import re
import random
import joblib
import os
from .models import *
import tensorflow as tf
import numpy as np
from datetime import datetime, timedelta
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from django.http import HttpResponse




# Create your views here.

class cityView(APIView):
    def get(self, request):
        allCities = City.objects.all().values()
        return HttpResponse({allCities})
    
    def post(self, request):
        City.objects.create(
                            id= request.data["id"],
                            name= request.data["name"],
                            lat= request.data["lat"],
                            lon= request.data["lon"]
                            )
        
        city = City.object.all().filter(id=request.data["id"]).values()
        return Response({"Message":"City Entry", "City:":city})


class ChatBotView(APIView):
    def handler(self, user_input):
        global data1,temperature_data,pests_data,cities,dates,temperature_model,pests_model,loaded_model,label_mapping
        with open("Z:\\Agritherm\\Agritherm\\Agritherm_data\\temp_data.json") as file:
            temperature_data = json.load(file)

        # Load the pests data from the JSON file
        with open("Z:\\Agritherm\\Agritherm\\Agritherm_data\\pests_data.json") as file:
            pests_data = json.load(file)

        # Load data from the third JSON file
        with open("Z:\\Agritherm\\Agritherm\\Agritherm_data\\data1.json") as file:
            data1 = json.load(file)    

        # Extract cities and dates from the temperature data
        cities = list(temperature_data.keys())
        dates = list(set([entry['date'] for city_data in temperature_data.values() for entry in city_data['data']]))
        # Create a mapping of heatwave labels to binary values
        label_mapping = {"False": 0, "True": 1}

        # Load the trained models
        temperature_model = tf.keras.models.load_model("Z:\\Agritherm\\Agritherm\\Agritherm_data\\temperature_model.h5")
        pests_model = tf.keras.models.load_model("Z:\\Agritherm\\Agritherm\\Agritherm_data\\pests_model.h5")
        loaded_model = joblib.load('Z:\\Agritherm\\Agritherm\\Agritherm_data\\Yield_Model.pkl')
        



    def generate_response(self, user_input):
        temperature_range_response = ""
        pests_response = ""
        temperature_response = ""
        crop_response = ""
        intents_response=None

        # Check if user input asks for temperature range
        if "temperature range" in user_input.lower():
            for crop in crops:
                if crop.lower() in user_input.lower():
                    temperature_range_response += random.choice([
        f"The recommended temperature range for {crop} is {temperature_ranges[crop]}.",
        f"Optimal temperature range for {crop} growth is {temperature_ranges[crop]}.",
        f"{crop} thrives in temperatures ranging from {temperature_ranges[crop]}.",
        f"{crop} requires a temperature range of {temperature_ranges[crop]} for optimal development."
    ])

        # Check if user input asks for pests
        if "pests" in user_input.lower():
            for crop in crops:
                if crop.lower() in user_input.lower():
                    pests_response += random.choice([
        f"Common pests that affect {crop} include {', '.join(pests[crop])}.",
        f"{crop} is prone to infestations by pests such as {', '.join(pests[crop])}.",
        f"Ensure proper pest management for {crop} to prevent damage from pests like {', '.join(pests[crop])}.",
        f"Protect your {crop} from common pests like {', '.join(pests[crop])} through effective pest control measures."
    ])
        
        intents = data1["intents"]   
        for intent in intents:
            patterns = intent["patterns"]
            responses = intent["responses"]
            if any(pattern.lower() in user_input.lower() for pattern in patterns):
                intents_response = random.choice(responses)  # Select a random response
                break

        else:
            intents_response = "I'm sorry, I didn't understand. Could you please rephrase?"
                
        # Extract city and date from user input
        city = None
        date = None
        for c in cities:
            if c.lower() in user_input.lower():
                city = c
                break

        for d in dates:
            if d in user_input:
                date = d
                break
        else:
            #Check if date keywords are mentioned
            today = datetime.now().strftime("%Y-%m-%d")
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

            if "yesterday" in user_input.lower():
                date = yesterday
            elif "tomorrow" in user_input.lower():
                date = tomorrow

            # Set the default date to today if not provided
            if not date:
                date = today

        # Generate response based on city and date
        if city and date:
            city_data = temperature_data[city]['data']
            for entry in city_data:
                if entry['date'] == date:
                    temperature = int(entry['temperatures'])
                    heatwave = label_mapping[entry['heatwave']]
                    temperature_prediction = temperature_model.predict(np.array([[temperature]]))
                    if temperature_prediction[0][0] >= 0.5:
                        if heatwave:
                            temperature_response = random.choice([
        f"{city} is currently experiencing a heatwave on {date} with a temperature of {temperature}°C.",
        f"The weather in {city} on {date} is {temperature}°C, and a heatwave is in effect.",
        f"A heatwave is ongoing in {city} on {date} with a temperature of {temperature}°C.",
        f"{city} is facing high temperatures on {date} with a heatwave prevailing at {temperature}°C.",
        f"On {date}, {city} is under a heatwave alert with temperatures reaching {temperature}°C."
    ])
                        else:
                            temperature_response = random.choice([
        f"{city} is experiencing normal weather conditions on {date} with a temperature of {temperature}°C.",
        f"The weather in {city} on {date} is {temperature}°C, and there is no heatwave.",
        f"On {date}, {city} is enjoying pleasant temperatures without any heatwave, measuring {temperature}°C.",
        f"{city} is having a moderate climate on {date} with temperatures around {temperature}°C, and no heatwave is expected.",
        f"No heatwave conditions are anticipated in {city} on {date} with a temperature of {temperature}°C."
    ])
                    break
            else:
                temperature_response = f"Data not available for {city} on {date}."

        # Combine temperature range , pests , temperature , yield responses
        response = ""
        if pests_response:
            response += pests_response
        if temperature_range_response:
            response += temperature_range_response
        if temperature_response:
            response += temperature_response
        if crop_response:
            response += crop_response
        if response == "" and intents_response is not None:
            response = intents_response
            
        return response
    def crop_predictor(self, hg_ha, avg_rain, pests_tonne, avg_temp):
        data_arr = []
            
        hg_ha = eval(hg_ha)
        avg_rain = eval(avg_rain)
        pests_tonne = float(pests_tonne)
        avg_temp = float(avg_temp)

        data_arr = [[hg_ha, avg_rain, pests_tonne, avg_temp]]
        # Make predictions using the loaded model
        prediction = loaded_model.predict(data_arr)
        prediction = str(prediction[0])
        # Format the response with the crop prediction
        crop = prediction.split(',')[0]
        try:
            soil = prediction.split(',')[1]
            crop_response = f"The predicted crop based on the given inputs is {crop} and the most suitable soil type for it is{soil}."
        except IndexError as e:
            crop_response = f"The predicted crop based on the given inputs is {crop}"

        return crop_response
    def extract_values(self, user_input):
        # Convert the user input to lowercase for case-insensitive matching
        user_input = user_input.lower()
        values = {}
        # check for digits in the input and assign them to each variable respectively 
        extracted_values = re.findall(r'\d+(?:\.\d+)?', user_input)
        hg_ha = extracted_values[0]
        avg_rain = extracted_values[1]
        pests_tonne = extracted_values[2]
        avg_temp = extracted_values[3]

        return hg_ha, avg_rain, pests_tonne, avg_temp

    
    def post(self, request):
        crops_syn = ['crop', 'crops', 'plant', 'plants']
        prompt_text = request.data.get("entry") # Extract the prompt text from the request data
        self.handler(prompt_text)
        if prompt_text.lower() in crops_syn:
            return HttpResponse('''I understand that you want me to predict suitable crops to be planted, to do this please give me the following information in the same format!
            \n 1. Yield in (hg/ha)\n 2. Average rainfall in (mm per year)\n 3. Pesticides in (tonnes)\n 4. Average temperature in (°C)\n''', content_type="application/json")
        if 'yield' in prompt_text.lower():
            values = self.extract_values(prompt_text)
            hg_ha = values[0]
            avg_rain = values[1]
            pests_tonne = values[2]
            avg_temp = values[3]
            
            response_text = self.crop_predictor(hg_ha, avg_rain, pests_tonne, avg_temp)
            response_data = {"response": response_text}
            json_response = json.dumps(response_data)
            return HttpResponse(json_response, content_type="application/json")
        else:
            self.handler(prompt_text)
            response_text = self.generate_response(prompt_text)
            #prompt = Prompt.objects.create(prompt=prompt_text)  # Create a new Prompt instance
            #response = Response.objects.create(response=response_text)  # Create a new Response instance
            response_data = {"response": response_text}
            json_response = json.dumps(response_data)
            return HttpResponse(json_response, content_type="application/json")  # Return a Response object with the response text
        
        
    def get(self, request):
        # Handle GET requests if required
        pass

