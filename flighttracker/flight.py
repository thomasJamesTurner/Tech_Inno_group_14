from enum import Enum
import location
import plane

class Flight_Status(Enum):
    GROUNDED        = 0
    DELAYED         = 1
    REFUELING       = 2
    BOARDING        = 3
    TAXIING         = 4
    ON_RUNWAY       = 5
    TAKING_OFF      = 6
    IN_FLIGHT       = 7
    LANDING         = 8

class Flight:
    call_sign = ""
    #model = plane()
    airline = ""
    speed =0
    altitude = 0
    eta = 0
    status = Flight_Status(0)
    current_location = location.Location(0,0)
    def __init__(self,callsign,speed,altitude,location):
        self.call_sign = callsign
        self.speed = speed
        self.altitude = altitude
        self.current_location = location

    def set_flight_status(self,status):
        self.status = status

    def add_location_to_route(self,place : location.Location):
        self.route.enqueue(place)

    def complete_leg(self):
        self.route.dequeue()

    def divert_flight(self,new_route):
        self.route = new_route
    
    def __str__(self):
        return f"{self.call_sign} — Altitude: {self.altitude} m\t Speed: {self.speed} m/s\t Location: ({self.current_location.latitude:.2f}, {self.current_location.longitude:.2f})\tstatus: {self.status}"

