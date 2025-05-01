import math

class Location:
    def __init__(self, longitude: float, latitude: float):
        self.longitude = longitude
        self.latitude = latitude

    def distance_to(self, location: 'Location') -> float:
        return math.sqrt(
            (self.longitude - location.longitude) ** 2 +
            (self.latitude - location.latitude) ** 2
        )

    def __str__(self):
        return f"({self.latitude:.4f}, {self.longitude:.4f})"
