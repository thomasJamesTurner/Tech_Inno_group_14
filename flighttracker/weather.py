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
            0: '☀️',
            1: '🌤️',
            2: '⛅', 
            3: '☁️', 
            45: '🌫️',
            48: '🌫️❄️',
            51: '🌦️', 
            53: '🌧️', 
            55: '🌧️', 
            56: '🌧️❄️',
            57: '🌧️❄️',
            61: '🌧️', 
            63: '🌧️', 
            65: '🌧️', 
            66: '🌧️❄️',
            67: '🌧️❄️',
            71: '🌨️',
            73: '🌨️',
            75: '❄️',
            77: '❄️',
            80: '🌦️',
            81: '🌧️',
            82: '⛈️',
            85: '🌨️',
            86: '❄️',
            95: '⛈️',
            96: '⛈️🌨️',
            99: '⛈️❄️'
        }
        return weather_codes.get(code, "Unknown weather code")
        
