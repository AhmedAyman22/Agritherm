import re
import json
import datetime
from sklearn.svm import SVC
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# Load the data from JSON files
with open('Z:\\Agritherm\\Agritherm\\Agritherm_data\\temp_data.json') as file:
    temp_data = json.load(file)

with open('Z:\\Agritherm\\Agritherm\\Agritherm_data\\pests_data.json') as file:
    pests_data = json.load(file)

with open('Z:\\Agritherm\\Agritherm\\Agritherm_data\\greetings_data.json') as file:
    greetings_data = json.load(file)

# Preprocess the data
documents = []
tags = []
responses = []

# Process temp_data
for location, data in temp_data.items():
    for item in data['data']:
        date = item.get('date', str(datetime.date.today()))
        temperature = item['temperatures']
        heatwave = item['heatwave']
        documents.append(f"{location} {date}")
        tags.append('temperature')


        suitable_crops = []
        for crop_item in pests_data:
            crop = crop_item['crop']
            temp_range = crop_item['temperature_range']
            if temperature >= int(temp_range.split('-')[0]) and temperature <= int(temp_range.split('-')[1]):
                suitable_crops.append(crop)

        if heatwave == "True":
            response = f"The temperature in {location} on {date} is {round(temperature,2)}°C. There is a Heatwave."
        else:
            response = f"The temperature in {location} on {date} is {round(temperature,2)}°C. There is no Heatwave."

        if suitable_crops:
            crop_list = ', '.join(suitable_crops)
            response += f"\nSuitable crops for this temperature range: {crop_list.split(',')[0:5]}."

        responses.append(response)

# Process pests_data
for item in pests_data:
    crop = item['crop']
    pests = item['pests']
    temp_range = item['temperature_range']
    documents.append(f"{crop} {pests}")
    tags.append('pests')
    response = f"For {crop}, beware of {', '.join(pests)} and The optimal temperature range for {crop} is {temp_range}°C."
    responses.append(response)

# Process greetings_data
if 'intents' in greetings_data:
    for intent in greetings_data['intents']:
        patterns = intent['patterns']
        responses.extend(intent['responses'])
        for pattern in patterns:
            documents.append(pattern.lower())
            tags.append(intent['tag'])
else:
    print("'intents' key does not exist in greetings_data dictionary.")

# Create TF-IDF vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

# Create SVM model
svm_model = SVC(kernel='linear')
svm_model.fit(X, tags)

# Chatbot interaction
def get_response(user_input):
    input_vector = vectorizer.transform([user_input.lower()])
    similarities = cosine_similarity(input_vector, X)
    most_similar_index = similarities.argmax()
    tag = svm_model.predict(input_vector)[0]
    if similarities[0, most_similar_index] > 0.5:
        return responses[most_similar_index]
    else:
        for intent in greetings_data['intents']:
            if intent['tag'] == tag:
                return intent['responses'][0]
    return greetings_data['intents'][-1]['responses'][0]  # Default response
def get_input(user_input):
    prompt = user_input
    return prompt
# Test the chatbot
def prompt_formatting(user_input):
    #user_input = input('User: ')
    if user_input.lower() in ['exit', 'quit']:
        break

    # Check if the user input contains a date in the format "YYYY-MM-DD"
    matches = re.search(r"\d{4}-\d{2}-\d{2}", user_input)
    if not matches:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = today + datetime.timedelta(days=1)

        if 'yesterday' in user_input.lower():
            user_input = user_input.replace('yesterday', str(yesterday))
        elif 'tomorrow' in user_input.lower():
            user_input = user_input.replace('tomorrow', str(tomorrow))
        else:
            user_input += f" {today}"

while True:
    user_input = input()
    user_input = get_input(user_input)
    user_input = prompt_formatting(user_input)
    response = get_response(user_input)
    return response