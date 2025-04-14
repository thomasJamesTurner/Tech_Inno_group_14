from enum import Enum
from queues import Queue
import location
import plane

class Flight_Status(Enum):
    DELAYED         = 0
    REFUELING       = 1
    BOARDING        = 2
    TAXIING         = 3
    ON_RUNWAY       = 4
    TAKING_OFF      = 5
    IN_FLIGHT       = 6
    LANDING         = 7

class Flight:
    call_sign = ""
    model = plane()
    airline = ""
    speed =0
    altitude = 0
    eta = 0
    status = Flight_Status(0)
    current_location = location.Location(0,0)
    route = Queue()

    def __init__(self):
        pass

    def add_location_to_route(self,place : location.Location):
        self.route.enqueue(place)

    def complete_leg(self):
        self.route.dequeue()

    def divert_flight(self,new_route):
        self.route = new_route

