from enum import Enum
from collections import deque
from geopy.distance import geodesic
import location


class Flight_Status(Enum):
    GROUNDED = 0
    DELAYED = 1
    REFUELING = 2
    BOARDING = 3
    TAXIING = 4
    ON_RUNWAY = 5
    TAKING_OFF = 6
    IN_FLIGHT = 7
    LANDING = 8


class Flight:
    def __init__(self, callsign, speed, altitude, location, airport_coords):
        self.call_sign = callsign
        self.speed = speed
        self.altitude = altitude
        self.current_location = location 
        self.status = Flight_Status.GROUNDED  # initial, can be updated later
        self.route = deque()
        self.airline = callsign[:3] if callsign else "Unknown"
        self.eta = None
        self.airport_coords = airport_coords 

    def set_flight_status(self, status):
        self.status = status
        self.set_eta()  # recalculate ETA whenever status changes

    def add_location_to_route(self, place: location.Location):
        self.route.append(place)

    def complete_leg(self):
        if self.route:
            self.route.popleft()

    def divert_flight(self, new_route):
        self.route = deque(new_route)

    def set_eta(self):
        if not self.airport_coords or not self.current_location:
            self.eta = None
            return

        try:
            distance_km = geodesic(
                (self.current_location.latitude, self.current_location.longitude),
                self.airport_coords
            ).km

            if isinstance(self.speed, (int, float)) and self.speed > 1:  # speed is in m/s
                speed_kms = self.speed / 1000.0  # convert to km/s
                eta_seconds = distance_km / speed_kms
                if eta_seconds > 0:
                    eta_minutes = eta_seconds / 60
                    self.eta = round(eta_minutes, 1)
                else:
                    self.eta = None
            else:
                self.eta = None
        except Exception as e:
            self.eta = None
            print(f"Error calculating ETA for {self.call_sign}: {e}")

    def __str__(self):
        return (
            f"{self.call_sign} — Altitude: {self.altitude} m\t"
            f"Speed: {self.speed} m/s\t"
            f"Location: ({self.current_location.latitude:.2f}, {self.current_location.longitude:.2f})\t"
            f"Status: {self.status.name}\t"
            f"ETA: {str(self.eta)+' min' if self.eta else 'N/A'}"
        )
