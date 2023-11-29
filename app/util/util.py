import os
import requests

class Util:
    OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
    POLLUTION_URL = "http://api.openweathermap.org/data/2.5/air_pollution"
    WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

    # This method is used to handle API requests and return JSON response
    @staticmethod
    def handle_api_request(url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request could not be completed. Error: {e}")
            return None

    # This method is used to get the pollution of the airport using the OpenWeather API
    @staticmethod
    def get_pollution_info(airport):
        latitude, longitude = str(airport["latitude_deg"]), str(
            airport["longitude_deg"]
        )
        pollution_point = 0

        response_json = Util.handle_api_request(
            f"{Util.POLLUTION_URL}?lat={latitude}&lon={longitude}&appid={Util.OPEN_WEATHER_API_KEY}"
        )

        if response_json and "list" in response_json and response_json["list"]:
            pollution_level = response_json["list"][0]["main"]["aqi"]
            pollution_point += pollution_level

            switcher = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
            pollution_level = switcher.get(pollution_level, "Invalid level")

        return {"pollution_level": pollution_level, "pollution_point": pollution_point}

    # This method is used to get the weather of the airport using the OpenWeather API
    @staticmethod
    def get_weather_info(airport):
        latitude, longitude = str(airport["latitude_deg"]), str(
            airport["longitude_deg"]
        )
        weather_point = 0

        response_json = Util.handle_api_request(
            f"{Util.WEATHER_URL}?lat={latitude}&lon={longitude}&appid={Util.OPEN_WEATHER_API_KEY}"
        )

        if response_json and "main" in response_json and "wind" in response_json:
            temperature = round(response_json["main"]["temp"] - 273.15)
            wind_speed = response_json["wind"]["speed"]

            if 0 <= temperature < 10 or 30 > temperature >= 25:
                weather_point += 1
            elif -5 < temperature < 0 or 35 > temperature >= 30:
                weather_point += 2
            elif temperature <= -5 or temperature >= 35:
                weather_point += 3
            if 7.9 > wind_speed > 0:
                weather_point += 0
            elif 10.8 > wind_speed >= 7.9:
                weather_point += 1
            elif 17.2 > wind_speed >= 10.8:
                weather_point += 3
            elif wind_speed >= 17.2:
                weather_point += 4

        return {
            "temperature": temperature,
            "wind_speed": wind_speed,
            "weather_point": weather_point,
        }


    @staticmethod
    def assign_rewards(airport, difficulty_level, reward_list):
        for reward in reward_list:
            if reward["difficult_level"] == difficulty_level:
                airport["needed_weapon"] = reward["passing_condition"]
                if reward["name"] == "energy":
                    airport["rewards_energy"] = reward["amount"]
                if reward["name"] == "weapon":
                    airport["rewards_weapon"] = reward["amount"]

    @staticmethod
    def update_airport_difficulty(airport, point, reward_list):
        if point >= 8:
            airport["difficulty_level"] = "hard"
            Util.assign_rewards(airport, "hard", reward_list)
        elif point > 4:
            airport["difficulty_level"] = "normal"
            Util.assign_rewards(airport, "normal", reward_list)
        else:
            airport["difficulty_level"] = "easy"
            Util.assign_rewards(airport, "easy", reward_list)

    @staticmethod
    def calculate_score(weapons_remaining, energy_remaining, time_remaining):
        # Calculate the score
        # The formula is: 
        # score = weapons_remaining + energy_remaining + time_remaining_in_minutes * 10
        calculated_score = 0
        if weapons_remaining > 0:
            calculated_score += weapons_remaining

        if energy_remaining > 0:
            calculated_score += energy_remaining

        if time_remaining > 0:
            calculated_score += time_remaining

        return calculated_score
