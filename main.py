import json
import requests
import os
from dotenv import load_dotenv # type: ignore
from concurrent.futures import ThreadPoolExecutor

# Load API key
load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Conditions for delay
DELAY_WEATHER = ["Rain", "Snow", "Extreme","Clouds"]


def get_weather(city):
    try:
        params = {
            "q": city,
            "appid": API_KEY
        }

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Error for {city}: {response.json().get('message')}")
            return None

        data = response.json()
        return data["weather"][0]["main"]

    except Exception as e:
        print(f"Exception for {city}: {e}")
        return None


def generate_apology(customer, city, weather):
    return f"Hi {customer}, your order to {city} is delayed due to {weather}. We appreciate your patience!"


def process_order(order):
    weather = get_weather(order["city"])

    if weather in DELAY_WEATHER:
        order["status"] = "Delayed"
        message = generate_apology(order["customer"], order["city"], weather)
        print(message)


# Load JSON
with open("orders.json", "r") as file:
    orders = json.load(file)

# Parallel API calls (IMPORTANT REQUIREMENT)
with ThreadPoolExecutor() as executor:
    executor.map(process_order, orders)

# Save updated JSON
with open("orders.json", "w") as file:
    json.dump(orders, file, indent=2)