from enum import Enum
import location

class Weather_Type(Enum):
    DRY             = 0
    LIGHT_RAIN      = 1
    HEAVY_RAIN      = 2
    HAIL            = 3
    STORM           = 4

class weather:
    wind_speed = 0.0
    wind_direction = None
    precipitation = 0.0
    weather_type  = Weather_Type(0)
    cloud_cover = 0.0
    visibility = 0.0
    def __init__(self,wind_direction : tuple[location.Location,location.Location],precipitation,weather_type : Weather_Type,cloud_cover,visibility):
        self.wind_direction = wind_direction
        self.wind_speed = wind_direction[0].distance_to(wind_direction[1])
        self.precipitation = precipitation
        self.weather_type = weather_type
        self.cloud_cover = cloud_cover
        self.visibility = visibility
        
