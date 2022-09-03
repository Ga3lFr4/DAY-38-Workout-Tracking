import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv("variables.env")

APP_ID = os.environ.get('APP_ID')
APP_KEY = os.environ.get('APP_KEY')

EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = "https://api.sheety.co/8ea934c3704cc59f230f19922252c500/workoutTracker/workouts"

HEADER = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY
}

params = {
    "query": input("Tell me what exercises you did: "),
    "gender": "male",
    "weight_kg": 75,
    "height_cm": 169,
    "age": 25,
}

response = requests.post(url=EXERCISE_ENDPOINT, headers=HEADER, json=params)

data = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
today_time = datetime.now().strftime("%X")

sheety_header = {
    "Authorization": os.environ.get('AUTHORIZATION'),
}

for exercise in data["exercises"]:
    sheety_params = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
    sheety_response = requests.post(SHEETY_ENDPOINT, headers=sheety_header, json=sheety_params)
    print(sheety_response.text)

