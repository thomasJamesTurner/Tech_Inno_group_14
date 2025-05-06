from enum import Enum
import flighttracker.location as location

class weather:
    wind_speed = 0.0
    wind_direction = None
    precipitation = 0.0
    weather_type  = 0
    cloud_cover = 0.0
    visibility = 0.0

    def __init__(self,wind_direction : tuple[location.Location,location.Location],precipitation,weather_type,cloud_cover,visibility):
        self.wind_direction = wind_direction
        self.wind_speed = wind_direction[0].distance_to(wind_direction[1])
        self.precipitation = precipitation
        self.weather_type = weather_type
        self.cloud_cover = cloud_cover
        self.visibility = visibility

    def weather_code_to_text(code):
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, "Unknown weather code")
        
