import math
class Location:
    longitude = None
    latitude = None
    def __init__(self,longitude,latitude):
        self.longitude  = longitude
        self.latitude   = latitude
    
    def distance_to(self,location):
        return math.sqrt((self.longitude - location.longitude)**2 + (self.latitude - location.latitude)**2)
